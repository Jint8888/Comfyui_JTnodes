"""
JT Nodes for ComfyUI - Custom nodes collection

A collection of custom nodes for ComfyUI providing various capabilities:
- Image processing (brightness adjustment)
- File management (custom image saving with path control)
- Text tools (serial number generator)
- AI integration (Siliconflow LLM API)

Author: JinT
Version: 1.1.0
License: MIT
"""

__version__ = "1.1.0"
__author__ = "JinT"
from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
