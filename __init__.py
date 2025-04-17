"""
JT Nodes for ComfyUI - Custom nodes collection

A collection of custom nodes for ComfyUI providing image processing capabilities:
- Brightness adjustment
- Custom image saving with path control

Author: JinT
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "JinT"
from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
