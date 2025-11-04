"""
主题管理器
"""
from enum import Enum
from typing import Dict
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette


class ThemeMode(Enum):
    """主题模式"""
    COMMON = "common"  # 常用主题（深色主题，当前主题）
    WHITE = "white"    # 白色主题（浅色主题，白色背景）


class ThemeManager:
    """主题管理器"""
    
    _instance = None
    _current_mode = ThemeMode.COMMON
    
    def __init__(self):
        self.mode = ThemeMode.COMMON
        self._initColors()
    
    def _initColors(self):
        """初始化颜色"""
        # 常用主题（深色主题，当前主题）
        self.common_colors = {
            "primary": QColor(0, 173, 239),      # 蓝色（#00ADEF）
            "secondary": QColor(122, 94, 255),   # 紫色（#7A5EFF）
            "background": QColor(30, 30, 42),    # 深灰蓝（#1E1E2A）
            "surface": QColor(42, 45, 58),      # 卡片背景（#2A2D3A）
            "text": QColor(255, 255, 255),       # 白色文字
            "text_secondary": QColor(169, 178, 193),  # 次要文字（#A9B2C1）
            "border": QColor(49, 52, 69),        # 分割线（#313445）
            "button": QColor(0, 173, 239),       # 按钮蓝色
            "button_hover": QColor(122, 94, 255), # 按钮紫色
            "button_pressed": QColor(0, 150, 210),
            "table_header": QColor(42, 45, 58),  # 表格头部（#2A2D3A）
            "table_row_even": QColor(37, 40, 55), # 表格行（#252837）
            "table_row_odd": QColor(37, 40, 55),
        }
        
        # 白色主题（浅色主题，白色背景）
        self.white_colors = {
            "primary": QColor(0, 173, 239),      # 蓝色（#00ADEF）
            "secondary": QColor(122, 94, 255),   # 紫色（#7A5EFF）
            "background": QColor(255, 255, 255), # 白色背景
            "surface": QColor(245, 245, 250),   # 卡片背景（浅灰）
            "text": QColor(30, 30, 42),         # 深色文字（#1E1E2A）
            "text_secondary": QColor(100, 100, 120),  # 次要文字
            "border": QColor(220, 220, 230),    # 分割线（浅灰）
            "button": QColor(0, 173, 239),       # 按钮蓝色
            "button_hover": QColor(122, 94, 255), # 按钮紫色
            "button_pressed": QColor(0, 150, 210),
            "table_header": QColor(245, 245, 250), # 表格头部（浅灰）
            "table_row_even": QColor(255, 255, 255), # 表格行（白色）
            "table_row_odd": QColor(250, 250, 255),
        }
    
    @classmethod
    def getInstance(cls):
        """获取单例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def getCurrentMode(self) -> ThemeMode:
        """获取当前主题模式"""
        return self._current_mode
    
    def setMode(self, mode: ThemeMode):
        """设置主题模式"""
        self._current_mode = mode
        self.mode = mode
    
    def getColor(self, color_name: str) -> QColor:
        """获取颜色"""
        colors = self.getColors()
        return colors.get(color_name, QColor(0, 0, 0))
    
    def getColors(self) -> Dict[str, QColor]:
        """获取所有颜色"""
        if self._current_mode == ThemeMode.COMMON:
            return self.common_colors
        elif self._current_mode == ThemeMode.WHITE:
            return self.white_colors
        else:
            return self.common_colors
    
    def applyTheme(self, widget):
        """应用主题到widget"""
        # 根据主题更新UIStyle的颜色
        from utils.ui_style import UIStyle
        
        if self._current_mode == ThemeMode.COMMON:
            # 常用主题（深色）- 恢复默认深色值
            UIStyle.BG_PRIMARY = "#1E1E2A"
            UIStyle.BG_SECONDARY = "#252837"
            UIStyle.BG_CARD = "#2A2D3A"
            UIStyle.BG_INPUT = "#2A2D3A"
            UIStyle.BG_DIVIDER = "#313445"
            UIStyle.TEXT_PRIMARY = "#FFFFFF"
            UIStyle.TEXT_SECONDARY = "#A9B2C1"
        elif self._current_mode == ThemeMode.WHITE:
            # 白色主题 - 更新为浅色值
            UIStyle.BG_PRIMARY = "#FFFFFF"
            UIStyle.BG_SECONDARY = "#FFFFFF"
            UIStyle.BG_CARD = "#F5F5FA"
            UIStyle.BG_INPUT = "#F5F5FA"
            UIStyle.BG_DIVIDER = "#DCDCE6"
            UIStyle.TEXT_PRIMARY = "#1E1E2A"
            UIStyle.TEXT_SECONDARY = "#646478"
        else:
            # 默认使用深色主题
            UIStyle.BG_PRIMARY = "#1E1E2A"
            UIStyle.BG_SECONDARY = "#252837"
            UIStyle.BG_CARD = "#2A2D3A"
            UIStyle.BG_INPUT = "#2A2D3A"
            UIStyle.BG_DIVIDER = "#313445"
            UIStyle.TEXT_PRIMARY = "#FFFFFF"
            UIStyle.TEXT_SECONDARY = "#A9B2C1"
        
        # 设置调色板
        palette = widget.palette()
        colors = self.getColors()
        
        palette.setColor(QPalette.ColorRole.Window, colors["background"])
        palette.setColor(QPalette.ColorRole.WindowText, colors["text"])
        palette.setColor(QPalette.ColorRole.Base, colors["surface"])
        palette.setColor(QPalette.ColorRole.AlternateBase, colors["table_row_odd"])
        palette.setColor(QPalette.ColorRole.Text, colors["text"])
        palette.setColor(QPalette.ColorRole.Button, colors["button"])
        palette.setColor(QPalette.ColorRole.ButtonText, colors["text"])
        palette.setColor(QPalette.ColorRole.Highlight, colors["primary"])
        palette.setColor(QPalette.ColorRole.HighlightedText, colors["text"])
        
        widget.setPalette(palette)
