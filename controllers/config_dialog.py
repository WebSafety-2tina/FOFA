"""
配置对话框
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup,
    QComboBox, QGroupBox, QMessageBox, QDialogButtonBox
)
from PySide6.QtCore import Qt
from pathlib import Path

from main.config import FofaConfig, ProxyConfig
from widgets.modern_button import ModernButton
from utils.ui_style import UIStyle


class ConfigDialog(QDialog):
    """配置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = FofaConfig.getInstance()
        self.proxy_config = ProxyConfig.getInstance()
        self.config_path = Path(__file__).parent.parent / "config.properties"
        
        self.initUI()
        self.loadConfig()
    
    def initUI(self):
        """初始化UI"""
        self.setWindowTitle("配置")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # 创建Tab
        tab_widget = QTabWidget()
        
        # FOFA配置Tab
        fofa_tab = self.createFofaTab()
        tab_widget.addTab(fofa_tab, "FOFA配置")
        
        # 代理配置Tab
        proxy_tab = self.createProxyTab()
        tab_widget.addTab(proxy_tab, "代理配置")
        
        layout.addWidget(tab_widget)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def createFofaTab(self) -> QWidget:
        """创建FOFA配置Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # API地址
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("FOFA API:"))
        self.api_input = QLineEdit()
        self.api_input.setText(self.config.API)
        api_layout.addWidget(self.api_input)
        layout.addLayout(api_layout)
        
        # API密钥
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("FOFA Key:"))
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setText(self.config.key)
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)
        
        # 最大条数
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Max Size:"))
        self.size_input = QLineEdit()
        self.size_input.setText(self.config.size)
        size_layout.addWidget(self.size_input)
        layout.addLayout(size_layout)
        
        # 检查剩余用量（使用按钮主题）
        check_group = QGroupBox("检查剩余用量")
        check_layout = QHBoxLayout()
        check_layout.setSpacing(10)
        
        self.check_enable_btn = ModernButton("启用", self)
        self.check_enable_btn.setCheckable(True)
        self.check_enable_btn.clicked.connect(lambda: self.check_disable_btn.setChecked(False))
        
        self.check_disable_btn = ModernButton("禁用", self)
        self.check_disable_btn.setCheckable(True)
        self.check_disable_btn.clicked.connect(lambda: self.check_enable_btn.setChecked(False))
        
        check_layout.addWidget(self.check_enable_btn)
        check_layout.addWidget(self.check_disable_btn)
        check_layout.addStretch()
        check_group.setLayout(check_layout)
        layout.addWidget(check_group)
        
        layout.addStretch()
        
        return widget
    
    def createProxyTab(self) -> QWidget:
        """创建代理配置Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 代理状态（使用按钮主题）
        status_group = QGroupBox("代理状态")
        status_layout = QHBoxLayout()
        status_layout.setSpacing(10)
        
        self.proxy_enable_btn = ModernButton("启用", self)
        self.proxy_enable_btn.setCheckable(True)
        self.proxy_enable_btn.clicked.connect(lambda: self.proxy_disable_btn.setChecked(False))
        
        self.proxy_disable_btn = ModernButton("禁用", self)
        self.proxy_disable_btn.setCheckable(True)
        self.proxy_disable_btn.clicked.connect(lambda: self.proxy_enable_btn.setChecked(False))
        
        status_layout.addWidget(self.proxy_enable_btn)
        status_layout.addWidget(self.proxy_disable_btn)
        status_layout.addStretch()
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # 代理类型（增加HTTPS选项）
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("代理类型:"))
        self.proxy_type_combo = QComboBox()
        self.proxy_type_combo.addItems(["HTTP", "HTTPS", "SOCKS5"])
        self.proxy_type_combo.setCurrentText(self.proxy_config.proxy_type)
        type_layout.addWidget(self.proxy_type_combo)
        layout.addLayout(type_layout)
        
        # 代理地址（统一输入框长度）
        ip_layout = QHBoxLayout()
        ip_label = QLabel("IP地址:")
        ip_label.setMinimumWidth(80)  # 统一标签宽度
        ip_label.setMaximumWidth(80)
        ip_layout.addWidget(ip_label)
        self.proxy_ip_input = QLineEdit()
        self.proxy_ip_input.setText(self.proxy_config.proxy_ip)
        self.proxy_ip_input.setMinimumWidth(200)  # 统一输入框最小宽度
        ip_layout.addWidget(self.proxy_ip_input)
        layout.addLayout(ip_layout)
        
        # 代理端口（统一输入框长度）
        port_layout = QHBoxLayout()
        port_label = QLabel("端口:")
        port_label.setMinimumWidth(80)
        port_label.setMaximumWidth(80)
        port_layout.addWidget(port_label)
        self.proxy_port_input = QLineEdit()
        self.proxy_port_input.setText(self.proxy_config.proxy_port)
        self.proxy_port_input.setMinimumWidth(200)  # 统一输入框最小宽度
        port_layout.addWidget(self.proxy_port_input)
        layout.addLayout(port_layout)
        
        # 代理用户名（统一输入框长度）
        user_layout = QHBoxLayout()
        user_label = QLabel("用户名:")
        user_label.setMinimumWidth(80)
        user_label.setMaximumWidth(80)
        user_layout.addWidget(user_label)
        self.proxy_user_input = QLineEdit()
        self.proxy_user_input.setText(self.proxy_config.proxy_user)
        self.proxy_user_input.setMinimumWidth(200)  # 统一输入框最小宽度
        user_layout.addWidget(self.proxy_user_input)
        layout.addLayout(user_layout)
        
        # 代理密码（统一输入框长度）
        password_layout = QHBoxLayout()
        password_label = QLabel("密码:")
        password_label.setMinimumWidth(80)
        password_label.setMaximumWidth(80)
        password_layout.addWidget(password_label)
        self.proxy_password_input = QLineEdit()
        self.proxy_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.proxy_password_input.setText(self.proxy_config.proxy_password)
        self.proxy_password_input.setMinimumWidth(200)  # 统一输入框最小宽度
        password_layout.addWidget(self.proxy_password_input)
        layout.addLayout(password_layout)
        
        layout.addStretch()
        
        return widget
    
    def loadConfig(self):
        """加载配置"""
        # 加载FOFA配置
        self.api_input.setText(self.config.API)
        self.key_input.setText(self.config.key)
        self.size_input.setText(self.config.size)
        
        if self.config.checkStatus:
            self.check_enable_btn.setChecked(True)
        else:
            self.check_disable_btn.setChecked(True)
        
        # 加载代理配置
        if self.proxy_config.status:
            self.proxy_enable_btn.setChecked(True)
        else:
            self.proxy_disable_btn.setChecked(True)
        
        self.proxy_type_combo.setCurrentText(self.proxy_config.proxy_type)
        self.proxy_ip_input.setText(self.proxy_config.proxy_ip)
        self.proxy_port_input.setText(self.proxy_config.proxy_port)
        self.proxy_user_input.setText(self.proxy_config.proxy_user)
        self.proxy_password_input.setText(self.proxy_config.proxy_password)
    
    def accept(self):
        """保存配置"""
        # 验证代理配置
        if self.proxy_enable_btn.isChecked():
            if not self.proxy_ip_input.text() or not self.proxy_port_input.text():
                QMessageBox.warning(self, "警告", "启用代理时，IP地址和端口不能为空")
                return
        
        # 更新配置
        self.config.API = self.api_input.text().strip()
        self.config.setKey(self.key_input.text().strip())
        self.config.setSize(self.size_input.text().strip())
        self.config.checkStatus = self.check_enable_btn.isChecked()
        
        self.proxy_config.status = self.proxy_enable_btn.isChecked()
        self.proxy_config.proxy_type = self.proxy_type_combo.currentText()
        self.proxy_config.proxy_ip = self.proxy_ip_input.text().strip()
        self.proxy_config.proxy_port = self.proxy_port_input.text().strip()
        self.proxy_config.proxy_user = self.proxy_user_input.text().strip()
        self.proxy_config.proxy_password = self.proxy_password_input.text().strip()
        
        # 保存到文件
        self.saveConfig()
        
        super().accept()
    
    def saveConfig(self):
        """保存配置到文件（properties格式）"""
        try:
            # 直接写入 properties 格式（key=value）
            with open(self.config_path, 'w', encoding='utf-8') as f:
                # 写入配置项
                f.write(f"api={self.config.API}\n")
                f.write(f"key={self.config.key}\n")
                f.write(f"max_size={self.config.size}\n")
                f.write(f"check_status={'on' if self.config.checkStatus else 'off'}\n")
                f.write(f"proxy_status={'on' if self.proxy_config.status else 'off'}\n")
                f.write(f"proxy_type={self.proxy_config.proxy_type}\n")
                f.write(f"proxy_ip={self.proxy_config.proxy_ip}\n")
                f.write(f"proxy_port={self.proxy_config.proxy_port}\n")
                f.write(f"proxy_user={self.proxy_config.proxy_user}\n")
                f.write(f"proxy_password={self.proxy_config.proxy_password}\n")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置失败: {str(e)}")

