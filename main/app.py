"""
FOFA Viewer主应用程序
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from controllers.main_controller import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion样式
    
    # 设置应用程序字体，确保UTF-8中文正确显示
    # 优先使用Microsoft YaHei UI，确保中文显示正常
    from PySide6.QtGui import QFont
    app_font = QFont()
    # 优先使用支持中文的字体
    app_font.setFamily("Microsoft YaHei UI, Microsoft YaHei, SimHei, PingFang SC, Segoe UI, Arial, sans-serif")
    app_font.setPixelSize(13)
    app_font.setStyleHint(QFont.StyleHint.SansSerif)
    # 确保字体支持中文
    app_font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
    app.setFont(app_font)
    
    # 设置应用程序信息
    app.setApplicationName("FOFA Viewer")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("WgpSec")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

