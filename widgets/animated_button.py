"""
动态按钮组件
"""
from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPainterPath, QColor, QPen, QFont
from utils.theme import ThemeManager


class AnimatedButton(QPushButton):
    """带动态效果的圆角按钮"""
    
    def __init__(self, text="", parent=None, radius=12):
        super().__init__(text, parent)
        self._radius = radius
        self._hovered = False
        self._pressed = False
        self._animation = None
        self._scale = 1.0
        
        self.setMinimumHeight(40)
        self.setMinimumWidth(100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        # 应用主题
        self.theme_manager = ThemeManager.getInstance()
        self.updateStyle()
    
    def setRadius(self, radius: int):
        """设置圆角半径"""
        self._radius = radius
        self.update()
    
    def updateStyle(self):
        """更新样式"""
        colors = self.theme_manager.getColors()
        self._button_color = colors["button"]
        self._hover_color = colors["button_hover"]
        self._pressed_color = colors["button_pressed"]
        self._text_color = colors["text"]
        self.update()
    
    def paintEvent(self, event):
        """绘制按钮"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        # 应用缩放
        if self._scale != 1.0:
            painter.translate(rect.center())
            painter.scale(self._scale, self._scale)
            painter.translate(-rect.center())
        
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)
        
        # 根据状态设置颜色
        if self._pressed:
            color = self._pressed_color
        elif self._hovered:
            color = self._hover_color
        else:
            color = self._button_color
        
        painter.fillPath(path, color)
        
        # 绘制文字
        painter.setPen(QPen(self._text_color))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
    
    def enterEvent(self, event):
        """鼠标进入"""
        self._hovered = True
        self.animateScale(1.05)
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开"""
        self._hovered = False
        self._pressed = False
        self.animateScale(1.0)
        self.update()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """鼠标按下"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self.animateScale(0.95)
            self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = False
            self.animateScale(1.0)
            self.update()
            if self.rect().contains(event.pos()):
                # 使用父类的clicked信号
                super().click()
        super().mouseReleaseEvent(event)
    
    def animateScale(self, target_scale: float):
        """动画改变缩放（使用定时器实现）"""
        if self._animation:
            self._animation.stop()
            self._animation.deleteLater()
        
        # 使用定时器实现平滑动画
        from PySide6.QtCore import QTimer
        
        start_scale = self._scale
        steps = 10
        current_step = 0
        
        def update_scale():
            nonlocal current_step
            if current_step <= steps:
                t = current_step / steps
                # 使用缓动函数
                ease_t = t * t * (3.0 - 2.0 * t)  # smoothstep
                self._scale = start_scale + (target_scale - start_scale) * ease_t
                self.update()
                current_step += 1
            else:
                self._scale = target_scale
                self.update()
                if self._animation:
                    self._animation.stop()
                    self._animation.deleteLater()
                    self._animation = None
        
        self._animation = QTimer(self)
        self._animation.timeout.connect(update_scale)
        self._animation.start(20)  # 每20ms更新一次

