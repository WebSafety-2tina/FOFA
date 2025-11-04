"""
样式化标签组件（使用按钮主题样式，但不可点击）
"""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPainterPath, QLinearGradient, QColor, QPen, QBrush
from utils.ui_style import UIStyle


class StyledLabel(QLabel):
    """样式化标签（按钮主题样式，但不可点击）"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(42)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        
        # 设置字体，确保中文正确显示
        font = self.font()
        font.setFamily("Microsoft YaHei UI, Microsoft YaHei, SimHei, PingFang SC, Segoe UI, Arial, sans-serif")
        font.setPixelSize(13)
        font.setStyleHint(font.StyleHint.SansSerif)
        font.setHintingPreference(font.HintingPreference.PreferDefaultHinting)
        self.setFont(font)
    
    def paintEvent(self, event):
        """绘制标签（使用按钮样式）"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(
            rect, 
            UIStyle.RADIUS_MEDIUM, 
            UIStyle.RADIUS_MEDIUM
        )
        
        # 创建渐变（与按钮样式一致）
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0, QColor(UIStyle.BTN_GRADIENT_START))
        gradient.setColorAt(1, QColor(UIStyle.BTN_GRADIENT_END))
        
        painter.fillPath(path, QBrush(gradient))
        
        # 绘制发光效果（轻微）
        glow_path = QPainterPath()
        glow_rect = rect.adjusted(-2, -2, 2, 2)
        glow_path.addRoundedRect(glow_rect, UIStyle.RADIUS_MEDIUM + 2, UIStyle.RADIUS_MEDIUM + 2)
        glow_color = QColor(UIStyle.BTN_GRADIENT_START)
        glow_color.setAlpha(50)  # 较低的透明度，表示不可点击
        painter.setPen(QPen(glow_color, 2))
        painter.drawPath(glow_path)
        
        # 绘制文字
        painter.setPen(QPen(QColor(UIStyle.TEXT_PRIMARY)))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())

