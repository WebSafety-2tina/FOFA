"""
现代风格按钮组件（带渐变和阴影效果）
"""
from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPainterPath, QLinearGradient, QColor, QPen, QBrush
from utils.ui_style import UIStyle


class ModernButton(QPushButton):
    """现代风格渐变按钮"""
    
    def __init__(self, text="", parent=None, gradient_start=None, gradient_end=None):
        super().__init__(text, parent)
        self.gradient_start = gradient_start or UIStyle.BTN_GRADIENT_START
        self.gradient_end = gradient_end or UIStyle.BTN_GRADIENT_END
        self._hovered = False
        self._pressed = False
        self._glow_intensity = 0.5
        
        self.setMinimumHeight(42)
        self.setMinimumWidth(100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 173, 239, 100))  # 蓝色阴影
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
    
    def paintEvent(self, event):
        """绘制按钮"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(
            QRectF(rect), 
            UIStyle.RADIUS_MEDIUM, 
            UIStyle.RADIUS_MEDIUM
        )
        
        # 创建渐变
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        
        # 检查是否为选中状态（checkable按钮）
        is_checked = self.isCheckable() and self.isChecked()
        
        if self._pressed or is_checked:
            # 按下时或选中时颜色更深
            gradient.setColorAt(0, QColor(self.gradient_end))
            gradient.setColorAt(1, QColor(self.gradient_start))
            glow_intensity = 0.8 if self._pressed else 1.0
        elif self._hovered:
            # 悬停时更亮
            start_color = QColor(self.gradient_start)
            end_color = QColor(self.gradient_end)
            start_color.setAlpha(255)
            end_color.setAlpha(255)
            gradient.setColorAt(0, start_color)
            gradient.setColorAt(1, end_color)
            glow_intensity = 1.0
        else:
            # 默认状态
            gradient.setColorAt(0, QColor(self.gradient_start))
            gradient.setColorAt(1, QColor(self.gradient_end))
            glow_intensity = 0.5
        
        painter.fillPath(path, QBrush(gradient))
        
        # 绘制发光效果
        if glow_intensity > 0:
            glow_path = QPainterPath()
            glow_rect = QRectF(rect.adjusted(-2, -2, 2, 2))
            glow_path.addRoundedRect(glow_rect, UIStyle.RADIUS_MEDIUM + 2, UIStyle.RADIUS_MEDIUM + 2)
            glow_color = QColor(self.gradient_start)
            glow_color.setAlpha(int(100 * glow_intensity))
            painter.setPen(QPen(glow_color, 2))
            painter.drawPath(glow_path)
        
        # 绘制文字
        painter.setPen(QPen(QColor(UIStyle.TEXT_PRIMARY)))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
    
    def enterEvent(self, event):
        """鼠标进入"""
        self._hovered = True
        self._animateGlow(1.0)
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开"""
        self._hovered = False
        self._pressed = False
        self._animateGlow(0.5)
        self.update()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """鼠标按下"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = False
            self.update()
        super().mouseReleaseEvent(event)
    
    def _animateGlow(self, target_intensity: float):
        """动画改变发光强度"""
        if hasattr(self, '_glow_animation') and self._glow_animation:
            self._glow_animation.stop()
        
        # 使用定时器实现动画
        from PySide6.QtCore import QTimer
        start_intensity = self._glow_intensity
        steps = 10
        current_step = [0]
        
        def updateGlow():
            if current_step[0] <= steps:
                t = current_step[0] / steps
                ease_t = t * t * (3.0 - 2.0 * t)  # smoothstep
                self._glow_intensity = start_intensity + (target_intensity - start_intensity) * ease_t
                self.update()
                current_step[0] += 1
            else:
                self._glow_intensity = target_intensity
                self.update()
                if hasattr(self, '_glow_timer') and self._glow_timer:
                    self._glow_timer.stop()
        
        self._glow_timer = QTimer(self)
        self._glow_timer.timeout.connect(updateGlow)
        self._glow_timer.start(20)  # 每20ms更新一次

