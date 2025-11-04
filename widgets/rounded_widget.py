"""
动态圆角UI组件
"""
from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QPainter, QPainterPath, QColor, QPen


class RoundedWidget(QFrame):
    """支持动态圆角的Widget"""
    
    def __init__(self, parent=None, radius=10):
        super().__init__(parent)
        self._radius = radius
        self._animation = None
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def setRadius(self, radius: int):
        """设置圆角半径"""
        self._radius = radius
        self.update()
    
    def radius(self) -> int:
        """获取圆角半径"""
        return self._radius
    
    def animateRadius(self, target_radius: int, duration: int = 300):
        """动画改变圆角半径"""
        if self._animation:
            self._animation.stop()
        
        self._animation = QPropertyAnimation(self, b"radius")
        self._animation.setDuration(duration)
        self._animation.setStartValue(self._radius)
        self._animation.setEndValue(target_radius)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._animation.start()
    
    def paintEvent(self, event):
        """绘制圆角"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 创建圆角路径
        path = QPainterPath()
        rect = self.rect()
        path.addRoundedRect(rect, self._radius, self._radius)
        
        # 设置裁剪区域
        painter.setClipPath(path)
        
        # 绘制背景
        if self.backgroundRole() != Qt.ColorRole.NoRole:
            painter.fillRect(rect, self.palette().color(self.backgroundRole()))
        
        # 绘制内容
        painter.setClipping(False)


class RoundedButton(QFrame):
    """圆角按钮"""
    
    def __init__(self, text="", parent=None, radius=8):
        super().__init__(parent)
        self._text = text
        self._radius = radius
        self._hovered = False
        self._pressed = False
        self.setMinimumHeight(32)
        self.setMinimumWidth(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def setRadius(self, radius: int):
        """设置圆角半径"""
        self._radius = radius
        self.update()
    
    def paintEvent(self, event):
        """绘制按钮"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)
        
        # 根据状态设置颜色
        if self._pressed:
            color = QColor(50, 120, 200)
        elif self._hovered:
            color = QColor(70, 140, 220)
        else:
            color = QColor(60, 130, 210)
        
        painter.fillPath(path, color)
        
        # 绘制文字
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self._text)
    
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
            if self.rect().contains(event.pos()):
                self.clicked.emit()
        super().mouseReleaseEvent(event)
    
    def enterEvent(self, event):
        """鼠标进入"""
        self._hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开"""
        self._hovered = False
        self._pressed = False
        self.update()
        super().leaveEvent(event)
    
    clicked = Signal()  # 点击信号


class RoundedLineEdit(QFrame):
    """圆角输入框"""
    
    def __init__(self, parent=None, radius=8):
        super().__init__(parent)
        self._radius = radius
        self._text = ""
        self._placeholder = ""
        self._focused = False
        self.setMinimumHeight(32)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def setRadius(self, radius: int):
        """设置圆角半径"""
        self._radius = radius
        self.update()
    
    def setPlaceholderText(self, text: str):
        """设置占位符"""
        self._placeholder = text
        self.update()
    
    def text(self) -> str:
        """获取文本"""
        return self._text
    
    def setText(self, text: str):
        """设置文本"""
        self._text = text
        self.update()
    
    def paintEvent(self, event):
        """绘制输入框"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)
        
        # 绘制边框
        border_color = QColor(100, 150, 200) if self._focused else QColor(180, 180, 180)
        painter.setPen(QPen(border_color, 2))
        painter.drawPath(path)
        
        # 绘制背景
        painter.fillPath(path, QColor(255, 255, 255))
        
        # 绘制文本或占位符
        text_rect = rect.adjusted(8, 0, -8, 0)
        if self._text:
            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._text)
        elif self._placeholder:
            painter.setPen(QPen(QColor(150, 150, 150)))
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._placeholder)
    
    def focusInEvent(self, event):
        """获得焦点"""
        self._focused = True
        self.update()
        super().focusInEvent(event)
    
    def focusOutEvent(self, event):
        """失去焦点"""
        self._focused = False
        self.update()
        super().focusOutEvent(event)
    
    def keyPressEvent(self, event):
        """键盘事件"""
        if event.key() == Qt.Key.Key_Backspace:
            self._text = self._text[:-1]
            self.update()
        elif event.text():
            self._text += event.text()
            self.update()
        super().keyPressEvent(event)

