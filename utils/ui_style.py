"""
UI样式定义
"""
from PySide6.QtGui import QColor


class UIStyle:
    """UI样式配置类"""
    
    # 颜色配置
    BG_PRIMARY = "#1E1E2A"  # 主背景
    BG_SECONDARY = "#252837"  # 表格背景
    BG_CARD = "#2A2D3A"  # 卡片背景
    BG_INPUT = "#2A2D3A"  # 输入框背景
    BG_DIVIDER = "#313445"  # 分割线
    
    TEXT_PRIMARY = "#FFFFFF"  # 主文字
    TEXT_SECONDARY = "#A9B2C1"  # 次要文字
    
    # 按钮渐变
    BTN_GRADIENT_START = "#00ADEF"  # 蓝
    BTN_GRADIENT_END = "#7A5EFF"  # 紫
    
    # Tab选中
    TAB_ACTIVE = "#00ADEF"
    TAB_HOVER = "#7A5EFF"
    
    # 状态颜色
    STATUS_SUCCESS = "#00FF88"
    STATUS_ERROR = "#FF4444"
    
    # 圆角半径
    RADIUS_SMALL = 8
    RADIUS_MEDIUM = 12
    RADIUS_LARGE = 16
    
    @staticmethod
    def getMainStyleSheet() -> str:
        """获取主样式表"""
        return f"""
            QMainWindow {{
                background-color: {UIStyle.BG_PRIMARY};
                color: {UIStyle.TEXT_PRIMARY};
            }}
            
            QWidget {{
                background-color: {UIStyle.BG_PRIMARY};
                color: {UIStyle.TEXT_PRIMARY};
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", "Arial", sans-serif;
                font-size: 13px;
            }}
            
            /* 顶部导航栏 */
            QMenuBar {{
                background-color: {UIStyle.BG_CARD};
                color: {UIStyle.TEXT_PRIMARY};
                padding: 10px;
                border-bottom: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
            }}
            
            QMenuBar::item {{
                background-color: transparent;
                padding: 8px 15px;
                border-radius: {UIStyle.RADIUS_SMALL}px;
            }}
            
            QMenuBar::item:selected {{
                background-color: {UIStyle.BG_DIVIDER};
            }}
            
            QMenu {{
                background-color: {UIStyle.BG_CARD};
                color: {UIStyle.TEXT_PRIMARY};
                border: 1px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                padding: 5px;
            }}
            
            QMenu::item {{
                padding: 8px 20px;
                border-radius: {UIStyle.RADIUS_SMALL}px;
            }}
            
            QMenu::item:selected {{
                background-color: {UIStyle.BG_DIVIDER};
            }}
            
            /* 输入框 */
            QLineEdit {{
                background-color: {UIStyle.BG_INPUT};
                color: {UIStyle.TEXT_PRIMARY};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                padding: 10px 15px;
                font-size: 14px;
            }}
            
            QLineEdit:focus {{
                border: 2px solid {UIStyle.BTN_GRADIENT_START};
                background-color: {UIStyle.BG_INPUT};
            }}
            
            /* 复选框 */
            QCheckBox {{
                color: {UIStyle.TEXT_SECONDARY};
                spacing: 8px;
                font-size: 13px;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: {UIStyle.RADIUS_SMALL}px;
                border: 2px solid {UIStyle.BG_DIVIDER};
                background-color: {UIStyle.BG_INPUT};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {UIStyle.BTN_GRADIENT_START};
                border-color: {UIStyle.BTN_GRADIENT_START};
            }}
            
            /* Tab标签 */
            QTabWidget::pane {{
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_LARGE}px;
                background-color: {UIStyle.BG_CARD};
                padding: 10px;
            }}
            
            QTabBar::tab {{
                background-color: {UIStyle.BG_SECONDARY};
                color: {UIStyle.TEXT_SECONDARY};
                padding: 10px 25px;
                margin-right: 5px;
                border-top-left-radius: {UIStyle.RADIUS_MEDIUM}px;
                border-top-right-radius: {UIStyle.RADIUS_MEDIUM}px;
                border: none;
                font-size: 14px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {UIStyle.BG_CARD};
                color: {UIStyle.TEXT_PRIMARY};
                border-bottom: 3px solid {UIStyle.BTN_GRADIENT_START};
            }}
            
            QTabBar::tab:hover {{
                background-color: {UIStyle.BG_DIVIDER};
            }}
            
            /* 表格 */
            QTableWidget {{
                background-color: {UIStyle.BG_SECONDARY};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_LARGE}px;
                gridline-color: {UIStyle.BG_DIVIDER};
                selection-background-color: {UIStyle.BTN_GRADIENT_START};
                selection-color: {UIStyle.TEXT_PRIMARY};
            }}
            
            QTableWidget::item {{
                padding: 10px;
                border: none;
                background-color: {UIStyle.BG_SECONDARY};
                color: {UIStyle.TEXT_PRIMARY};
            }}
            
            QTableWidget::item:selected {{
                background-color: {UIStyle.BTN_GRADIENT_START};
                color: {UIStyle.TEXT_PRIMARY};
            }}
            
            QHeaderView::section {{
                background-color: {UIStyle.BG_CARD};
                color: {UIStyle.TEXT_PRIMARY};
                padding: 12px;
                border: none;
                border-bottom: 2px solid {UIStyle.BG_DIVIDER};
                font-weight: bold;
                font-size: 13px;
            }}
            
            /* 状态栏 */
            QStatusBar {{
                background-color: rgba(42, 45, 58, 0.8);
                color: {UIStyle.TEXT_SECONDARY};
                border-top: 1px solid {UIStyle.BG_DIVIDER};
                padding: 5px;
            }}
            
            /* GroupBox */
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_LARGE}px;
                margin-top: 10px;
                padding-top: 15px;
                font-size: 14px;
                color: {UIStyle.TEXT_PRIMARY};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
            
            /* Label */
            QLabel {{
                color: {UIStyle.TEXT_PRIMARY};
                font-size: 14px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", "Arial", sans-serif;
                padding: 0px;
                margin: 0px;
            }}
            
            /* GroupBox标题 */
            QGroupBox::title {{
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", "Arial", sans-serif;
            }}
            
            /* 表格表头 */
            QHeaderView::section {{
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", "Arial", sans-serif;
            }}
            
            /* 表格内容 */
            QTableWidget {{
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", "Arial", sans-serif;
            }}
        """

