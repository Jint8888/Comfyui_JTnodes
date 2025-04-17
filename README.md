# Comfyui JTnodes

这个项目包含了一些自定义的ComfyUI节点，用于图像处理任务。

## 功能

目前包含以下节点：

- **JT Brightness Adjustment**: 一个简单的图像亮度调节节点
  - 输入：
    - 图像 (IMAGE)
    - 亮度调节系数 (0.0 到 2.0)
  - 输出：
    - 处理后的图像 (IMAGE)

- **JT Save Image to Path**: 增强型图像保存节点
  - 输入：
    - 图像 (IMAGE)
    - 文件夹路径 (STRING，默认: "/path")
    - 文件名 (STRING，默认: "Image")
    - 格式 (COMBO ["PNG", "JPG"]，默认: "JPG")
    - 使用序号 (BOOLEAN，默认: False)
    - 分隔符 (COMBO ["none", "hyphen", "underscore"]，默认: "hyphen")
      - none: 无分隔符
      - hyphen: 连字符 (-)
      - underscore: 下划线 (_)
    - 序号位数 (INT，1-5位，默认: 4)
    - 允许覆盖 (BOOLEAN，默认: True)
  - 输出：
    - 原始图像传递 (IMAGE) - 用于工作流程继续
    - 保存文件夹路径 (STRING) - 图像保存的目录完整路径
    - 保存文件名列表 (STRING) - 所有保存的文件名，每个文件名占一行
    - 保存数量 (INT) - 本次保存的图像总数

  - 文件命名规则：
    1. 无序号模式：
       - 直接使用输入的文件名保存
       - 当不允许覆盖且文件存在时跳过保存
    
    2. 序号模式：
       - 使用 文件名 + 分隔符 + 序号 的格式
       - 序号位数在1-5位之间自动调整
       - 允许覆盖时：从1开始按顺序编号
       - 不允许覆盖时：从1开始查找未被使用的序号
    
    3. 批量保存时：
       - 允许覆盖：使用连续的序号
       - 不允许覆盖：自动跳过已存在的序号

  - 特点：
    - 自动创建完整的输出目录结构
    - 提供完整的文件名列表预览
    - 支持PNG格式的元数据保存
    - 高质量的图像保存（JPG使用95质量）
    - 实时显示所有保存文件名，每行一个
    - 智能的序号管理系统
    - 灵活的覆盖控制

## 安装说明

1. 找到你的ComfyUI安装目录
2. 进入 `custom_nodes` 目录（如果不存在则创建）
3. 将此项目克隆或复制到该目录：
   ```bash
   cd custom_nodes
   # 通过克隆仓库
   git clone [你的仓库URL]
   # 或直接将 Comfyui_JTnodes 文件夹复制到此目录
   ```
4. 重启ComfyUI

## 使用方法

1. 启动ComfyUI
2. 在节点选择菜单中，查找对应节点（在JT分类下）
3. 将节点添加到你的工作流中
4. 设置所需参数
5. 运行工作流

## 开发新节点

如果你想添加新的节点，可以按照以下步骤：

1. 在 `nodes.py` 中创建新的节点类
2. 实现必要的接口：
   - INPUT_TYPES() - 定义输入参数
   - RETURN_TYPES - 定义输出类型
   - FUNCTION - 处理函数名称
   - CATEGORY - 节点分类
3. 在 NODE_CLASS_MAPPINGS 和 NODE_DISPLAY_NAME_MAPPINGS 中注册新节点

## 要求

- ComfyUI
- PyTorch
- NumPy
- Pillow(PIL)

## 许可证

MIT License
