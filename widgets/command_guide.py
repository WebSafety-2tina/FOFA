"""
命令指南组件
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from utils.ui_style import UIStyle


class CommandGuide(QWidget):
    """命令指南组件"""
    command_clicked = Signal(str)  # 命令点击信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题
        title = QLabel("命令指南")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {UIStyle.TEXT_PRIMARY};
                padding: 10px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
        """)
        layout.addWidget(title)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                background-color: {UIStyle.BG_CARD};
            }}
            QScrollBar:vertical {{
                background-color: {UIStyle.BG_SECONDARY};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {UIStyle.BTN_GRADIENT_START};
                border-radius: 6px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {UIStyle.BTN_GRADIENT_END};
            }}
        """)
        
        # 内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(15, 15, 15, 15)
        
        # 逻辑连接符
        self.addLogicalOperators(content_layout)
        
        # 基础类
        self.addGeneralCommands(content_layout)
        
        # 标记类
        self.addSpecialLabelCommands(content_layout)
        
        # 协议类
        self.addProtocolCommands(content_layout)
        
        # 网站类
        self.addWebsiteCommands(content_layout)
        
        # 地理位置
        self.addLocationCommands(content_layout)
        
        # 证书类
        self.addCertificateCommands(content_layout)
        
        # 时间类
        self.addTimeCommands(content_layout)
        
        # 独立IP语法
        self.addIPCommands(content_layout)
        
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
    
    def addLogicalOperators(self, layout):
        """添加逻辑连接符"""
        group = QGroupBox("逻辑连接符")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                margin-top: 10px;
                padding-top: 15px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        group_layout = QVBoxLayout()
        
        operators = [
            ("=", "匹配，=\"\"时，可查询不存在字段或者值为空的情况。"),
            ("==", "完全匹配，==\"\"时，可查询存在且值为空的情况。"),
            ("&&", "与"),
            ("||", "或"),
            ("!=", "不匹配，!=\"\"时，可查询值不为空的情况。"),
            ("*=", "模糊匹配，使用*或者?进行搜索。"),
            ("()", "确认查询优先级，括号内容优先级最高。"),
        ]
        
        for op, desc in operators:
            btn = QPushButton(f"{op} - {desc}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_START}, 
                        stop:1 {UIStyle.BTN_GRADIENT_END});
                    color: {UIStyle.TEXT_PRIMARY};
                    border-radius: {UIStyle.RADIUS_SMALL}px;
                    padding: 8px;
                    text-align: left;
                    font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_END}, 
                        stop:1 {UIStyle.BTN_GRADIENT_START});
                }}
            """)
            btn.clicked.connect(lambda checked, o=op: self.command_clicked.emit(o))
            group_layout.addWidget(btn)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def addGeneralCommands(self, layout):
        """添加基础类命令"""
        group = QGroupBox("基础类（General）")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                margin-top: 10px;
                padding-top: 15px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        group_layout = QVBoxLayout()
        
        commands = [
            ('ip="1.1.1.1"', '通过单一IPv4地址进行查询'),
            ('ip="220.181.111.1/24"', '通过IPv4 C段进行查询'),
            ('port="6379"', '通过端口号进行查询'),
            ('domain="qq.com"', '通过根域名进行查询'),
            ('host=".fofa.info"', '通过主机名进行查询'),
            ('os="centos"', '通过操作系统进行查询'),
            ('server="Microsoft-IIS/10"', '通过服务器进行查询'),
            ('asn="19551"', '通过自治系统号进行搜索'),
            ('org="LLC Baxet"', '通过所属组织进行查询'),
            ('is_domain=true', '筛选拥有域名的资产'),
            ('is_ipv6=true', '筛选是ipv6的资产'),
        ]
        
        for cmd, desc in commands:
            btn = QPushButton(f"{cmd} - {desc}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_START}, 
                        stop:1 {UIStyle.BTN_GRADIENT_END});
                    color: {UIStyle.TEXT_PRIMARY};
                    border-radius: {UIStyle.RADIUS_SMALL}px;
                    padding: 8px;
                    text-align: left;
                    font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_END}, 
                        stop:1 {UIStyle.BTN_GRADIENT_START});
                }}
            """)
            btn.clicked.connect(lambda checked, c=cmd: self.command_clicked.emit(c))
            group_layout.addWidget(btn)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def addSpecialLabelCommands(self, layout):
        """添加标记类命令"""
        group = QGroupBox("标记类（Special Label）")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                margin-top: 10px;
                padding-top: 15px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        group_layout = QVBoxLayout()
        
        commands = [
            ('app="Microsoft-Exchange"', '通过FOFA整理的规则进行查询'),
            ('fid="sSXXGNUO2FefBTcCLIT/2Q=="', '通过FOFA聚合的站点指纹进行查询'),
            ('product="NGINX"', '通过FOFA标记的产品名进行查询'),
            ('category="服务"', '通过FOFA标记的分类进行查询'),
            ('cloud_name="Aliyundun"', '通过云服务商进行查询'),
            ('is_cloud=true', '筛选是云服务的资产'),
            ('is_honeypot=false', '筛选不是蜜罐的资产'),
        ]
        
        for cmd, desc in commands:
            btn = QPushButton(f"{cmd} - {desc}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_START}, 
                        stop:1 {UIStyle.BTN_GRADIENT_END});
                    color: {UIStyle.TEXT_PRIMARY};
                    border-radius: {UIStyle.RADIUS_SMALL}px;
                    padding: 8px;
                    text-align: left;
                    font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_END}, 
                        stop:1 {UIStyle.BTN_GRADIENT_START});
                }}
            """)
            btn.clicked.connect(lambda checked, c=cmd: self.command_clicked.emit(c))
            group_layout.addWidget(btn)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def addProtocolCommands(self, layout):
        """添加协议类命令"""
        group = QGroupBox("协议类（type=service）")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                margin-top: 10px;
                padding-top: 15px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        group_layout = QVBoxLayout()
        
        commands = [
            ('protocol="quic"', '通过协议名称进行查询'),
            ('banner="users"', '通过协议返回信息进行查询'),
            ('banner_hash="7330105010150477363"', '通过协议响应体计算的hash值进行查询'),
            ('base_protocol="udp"', '查询传输层为udp协议的资产'),
        ]
        
        for cmd, desc in commands:
            btn = QPushButton(f"{cmd} - {desc}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_START}, 
                        stop:1 {UIStyle.BTN_GRADIENT_END});
                    color: {UIStyle.TEXT_PRIMARY};
                    border-radius: {UIStyle.RADIUS_SMALL}px;
                    padding: 8px;
                    text-align: left;
                    font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_END}, 
                        stop:1 {UIStyle.BTN_GRADIENT_START});
                }}
            """)
            btn.clicked.connect(lambda checked, c=cmd: self.command_clicked.emit(c))
            group_layout.addWidget(btn)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def addWebsiteCommands(self, layout):
        """添加网站类命令"""
        group = QGroupBox("网站类（type=subdomain）")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                margin-top: 10px;
                padding-top: 15px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        group_layout = QVBoxLayout()
        
        commands = [
            ('title="beijing"', '通过网站标题进行查询'),
            ('header="elastic"', '通过响应标头进行查询'),
            ('header_hash="1258854265"', '通过http/https响应头计算的hash值进行查询'),
            ('body="网络空间测绘"', '通过HTML正文进行查询'),
            ('icon_hash="-247388890"', '通过网站图标的hash值进行查询'),
            ('status_code="402"', '筛选服务状态为402的服务（网站）资产'),
            ('icp="京ICP证030173号"', '通过HTML正文包含的ICP备案号进行查询'),
        ]
        
        for cmd, desc in commands:
            btn = QPushButton(f"{cmd} - {desc}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_START}, 
                        stop:1 {UIStyle.BTN_GRADIENT_END});
                    color: {UIStyle.TEXT_PRIMARY};
                    border-radius: {UIStyle.RADIUS_SMALL}px;
                    padding: 8px;
                    text-align: left;
                    font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_END}, 
                        stop:1 {UIStyle.BTN_GRADIENT_START});
                }}
            """)
            btn.clicked.connect(lambda checked, c=cmd: self.command_clicked.emit(c))
            group_layout.addWidget(btn)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def addLocationCommands(self, layout):
        """添加地理位置命令"""
        group = QGroupBox("地理位置（Location）")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                margin-top: 10px;
                padding-top: 15px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        group_layout = QVBoxLayout()
        
        commands = [
            ('country="CN"', '通过国家的简称代码进行查询'),
            ('country="中国"', '通过国家中文名称进行查询'),
            ('region="Zhejiang"', '通过省份/地区英文名称进行查询'),
            ('region="浙江"', '通过省份/地区中文名称进行查询（仅支持中国地区）'),
            ('city="Hangzhou"', '通过城市英文名称进行查询'),
        ]
        
        for cmd, desc in commands:
            btn = QPushButton(f"{cmd} - {desc}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_START}, 
                        stop:1 {UIStyle.BTN_GRADIENT_END});
                    color: {UIStyle.TEXT_PRIMARY};
                    border-radius: {UIStyle.RADIUS_SMALL}px;
                    padding: 8px;
                    text-align: left;
                    font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_END}, 
                        stop:1 {UIStyle.BTN_GRADIENT_START});
                }}
            """)
            btn.clicked.connect(lambda checked, c=cmd: self.command_clicked.emit(c))
            group_layout.addWidget(btn)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def addCertificateCommands(self, layout):
        """添加证书类命令"""
        group = QGroupBox("证书类（Certificate）")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                margin-top: 10px;
                padding-top: 15px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        group_layout = QVBoxLayout()
        
        commands = [
            ('cert="baidu"', '通过证书进行查询'),
            ('cert.subject="Oracle Corporation"', '通过证书的持有者进行查询'),
            ('cert.issuer="DigiCert"', '通过证书的颁发者进行查询'),
            ('cert.subject.cn="baidu.com"', '通过证书持有者的通用名称进行查询'),
            ('cert.domain="huawei.com"', '通过证书持有者的根域名进行查询'),
            ('cert.sn="356078156165546797850343536942784588840297"', '通过证书序列号进行查询'),
            ('jarm="2ad2ad0002ad2ad22c2ad2ad2ad2ad2eac92ec34bcc0cf7520e97547f83e81"', '通过JARM指纹进行查询'),
        ]
        
        for cmd, desc in commands:
            btn = QPushButton(f"{cmd} - {desc}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_START}, 
                        stop:1 {UIStyle.BTN_GRADIENT_END});
                    color: {UIStyle.TEXT_PRIMARY};
                    border-radius: {UIStyle.RADIUS_SMALL}px;
                    padding: 8px;
                    text-align: left;
                    font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_END}, 
                        stop:1 {UIStyle.BTN_GRADIENT_START});
                }}
            """)
            btn.clicked.connect(lambda checked, c=cmd: self.command_clicked.emit(c))
            group_layout.addWidget(btn)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def addTimeCommands(self, layout):
        """添加时间类命令"""
        group = QGroupBox("时间类（Last update time）")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                margin-top: 10px;
                padding-top: 15px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        group_layout = QVBoxLayout()
        
        commands = [
            ('after="2023-01-01"', '筛选某一时间之后有更新的资产'),
            ('before="2023-12-01"', '筛选某一时间之前有更新的资产'),
            ('after="2023-01-01" && before="2023-12-01"', '筛选某一时间区间有更新的资产'),
        ]
        
        for cmd, desc in commands:
            btn = QPushButton(f"{cmd} - {desc}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_START}, 
                        stop:1 {UIStyle.BTN_GRADIENT_END});
                    color: {UIStyle.TEXT_PRIMARY};
                    border-radius: {UIStyle.RADIUS_SMALL}px;
                    padding: 8px;
                    text-align: left;
                    font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_END}, 
                        stop:1 {UIStyle.BTN_GRADIENT_START});
                }}
            """)
            btn.clicked.connect(lambda checked, c=cmd: self.command_clicked.emit(c))
            group_layout.addWidget(btn)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def addIPCommands(self, layout):
        """添加独立IP语法命令"""
        group = QGroupBox("独立IP语法（独立IP系列语法，不可和上面其他语法共用）")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_MEDIUM}px;
                margin-top: 10px;
                padding-top: 15px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        group_layout = QVBoxLayout()
        
        commands = [
            ('port_size="6"', '筛选开放端口数量等于6个的独立IP'),
            ('port_size_gt="6"', '筛选开放端口数量大于6个的独立IP'),
            ('port_size_lt="12"', '筛选开放端口数量小于12个的独立IP'),
            ('ip_ports="80,161"', '筛选同时开放不同端口的独立IP'),
            ('ip_country="CN"', '通过国家的简称代码进行查询独立IP'),
        ]
        
        for cmd, desc in commands:
            btn = QPushButton(f"{cmd} - {desc}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_START}, 
                        stop:1 {UIStyle.BTN_GRADIENT_END});
                    color: {UIStyle.TEXT_PRIMARY};
                    border-radius: {UIStyle.RADIUS_SMALL}px;
                    padding: 8px;
                    text-align: left;
                    font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {UIStyle.BTN_GRADIENT_END}, 
                        stop:1 {UIStyle.BTN_GRADIENT_START});
                }}
            """)
            btn.clicked.connect(lambda checked, c=cmd: self.command_clicked.emit(c))
            group_layout.addWidget(btn)
        
        group.setLayout(group_layout)
        layout.addWidget(group)

