"""
JTnodes implementation for ComfyUI - Optimized version
"""
import os
import re
import json
import torch
import numpy as np
from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngInfo

class JTBrightnessNode:
    """
    A basic image processing node that adjusts image brightness
    
    Returns:
        IMAGE: Processed image with adjusted brightness
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define the input types for the node"""
        return {
            "required": {
                "image": ("IMAGE",),
                "brightness": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process_image"
    CATEGORY = "JT/image"

    def process_image(self, image, brightness):
        """
        Adjust the brightness of the input image
        
        Args:
            image: Input image tensor (B, H, W, C)
            brightness: Brightness adjustment factor (float between 0.0 and 2.0)
        
        Returns:
            Processed image tensor with adjusted brightness
        """
        # 验证输入
        if not isinstance(image, torch.Tensor):
            raise ValueError("Expected image to be a torch.Tensor")
        
        # 应用亮度调整并限制在有效范围内
        # 使用torch内联操作提高性能
        return (torch.clamp(image * float(brightness), 0.0, 1.0),)

class JTImagesavetopath:
    """
    Enhanced image saver with flexible naming options
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define the input types for the node"""
        return {
            "required": {
                "image": ("IMAGE",),
                "folder_path": ("STRING", {
                    "default": "/path",
                    "multiline": False
                }),
                "filename": ("STRING", {
                    "default": "Image",
                    "multiline": False
                }),
                "format": (["PNG", "JPG"], {
                    "default": "JPG"
                }),
                "use_counter": ("BOOLEAN", {
                    "default": False,
                    "label": "使用序号"
                }),
                "separator": (["none", "hyphen", "underscore"], {
                    "default": "hyphen",
                    "label": "分隔符"
                }),
                "counter_digits": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "label": "序号位数(1-5)"
                }),
                "allow_overwrite": ("BOOLEAN", {
                    "default": True,
                    "label": "允许覆盖"
                }),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "INT")
    RETURN_NAMES = ("image", "save_folder", "save_filename", "save_count")
    FUNCTION = "save_image"
    CATEGORY = "JT/image"

    def _get_save_path(self, folder_path: Path, filename: str, extension: str,
                      use_counter: bool, separator_type: str, digits: int,
                      allow_overwrite: bool, index: int = 0) -> Path:
        """生成保存路径"""
        # 处理基本文件路径（不带序号）
        base_path = folder_path / f"{filename}{extension}"
        if not use_counter:
            return None if not allow_overwrite and base_path.exists() else base_path
            
        # 获取分隔符并处理序号位数
        separator = {"none": "", "hyphen": "-", "underscore": "_"}[separator_type]
        digits = min(max(digits, 1), 5)  # 限制在1-5位之间
        current_number = index + 1

        # 生成带序号的文件名
        def get_path(num): 
            return folder_path / f"{filename}{separator}{num:0{digits}d}{extension}"
            
        # 允许覆盖时直接使用当前序号
        if allow_overwrite:
            return get_path(current_number)
            
        # 不允许覆盖时查找可用序号
        save_path = get_path(current_number)
        while save_path.exists():
            current_number += 1
            save_path = get_path(current_number)
            
        return save_path
    
    def save_image(self, image, folder_path, filename, format, use_counter, 
                  separator, counter_digits, allow_overwrite, prompt=None, extra_pnginfo=None):
        """Save images with advanced naming options"""
        # 输入验证
        if not isinstance(image, torch.Tensor):
            raise ValueError("Expected image to be a torch.Tensor")
        if not (filename := filename.strip()):
            raise ValueError("Filename cannot be empty")
        
        # 初始化保存环境
        folder_path = Path(folder_path)
        folder_path.mkdir(parents=True, exist_ok=True)
        extension = ".png" if format == "PNG" else ".jpg"
        
        # 处理图像数据
        images = image.cpu().numpy()
        if len(images.shape) == 3:
            images = images[np.newaxis, ...]
            
        saved_paths = []
        
        # 生成文件路径并保存图片
        for idx in range(images.shape[0]):
            save_path = self._get_save_path(
                folder_path, filename, extension,
                use_counter, separator, counter_digits,
                allow_overwrite, idx
            )
            
            if save_path is None:  # 不允许覆盖且文件存在
                continue
                
            # 转换并保存图片
            img = Image.fromarray((images[idx] * 255).clip(0, 255).astype(np.uint8))
            
            # 设置保存参数
            save_params = {
                "format": "PNG" if format == "PNG" else "JPEG",
                "quality": 95 if format == "JPG" else None
            }
            
            # 添加PNG元数据
            if format == "PNG" and (prompt or extra_pnginfo):
                pnginfo = PngInfo()
                if prompt:
                    pnginfo.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo:
                    pnginfo.add_text("workflow", json.dumps(extra_pnginfo))
                save_params["pnginfo"] = pnginfo
                
            img.save(save_path, **save_params)
            saved_paths.append(save_path)
        
        # 返回结果
        return (
            image,                          # 原始图像
            str(folder_path.absolute()),    # 保存目录
            "\n".join(p.name for p in saved_paths) if saved_paths else "",  # 文件名列表
            len(saved_paths)                # 保存数量
        )

NODE_CLASS_MAPPINGS = {
    "JTBrightnessAdjustment": JTBrightnessNode,
    "JTImagesavetopath": JTImagesavetopath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JTBrightnessAdjustment": "JT Brightness Adjustment",
    "JTImagesavetopath": "JT Save Image to Path"
}
