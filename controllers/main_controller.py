"""
主窗口控制器
"""
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QLineEdit, QCheckBox,
    QLabel, QMenuBar, QMenu, QMessageBox, QFileDialog,
    QAbstractItemView, QGroupBox, QStatusBar, QApplication
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QUrl
from PySide6.QtGui import QAction, QIcon, QDesktopServices

from main.config import FofaConfig, ProxyConfig
from utils.request_util import RequestUtil
from utils.data_util import DataUtil
from models.table_bean import TableBean, ExcelBean, TabDataBean
from widgets.modern_button import ModernButton
from widgets.styled_label import StyledLabel
from widgets.command_guide import CommandGuide
from utils.theme import ThemeManager, ThemeMode
from utils.ui_style import UIStyle


class QueryThread(QThread):
    """查询线程"""
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.url = url
        self.request_util = RequestUtil.getInstance()
    
    def run(self):
        """执行查询"""
        try:
            result = self.request_util.getHTML(self.url, 120000, 120000)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.config = FofaConfig.getInstance()
        self.request_util = RequestUtil.getInstance()
        self.data_util = DataUtil()
        
        # 加载配置
        DataUtil.loadConfigure()
        
        # Tab数据字典 {tab_title: TabDataBean}
        self.tab_data = {}
        
        # 线程列表（用于管理线程）
        self.threads = []
        
        # 主题管理器
        self.theme_manager = ThemeManager.getInstance()
        
        # 初始化UI
        self.initUI()
        
        # 初始化首页
        self.initHomePage()
        
        # 应用主题
        self.applyTheme()
    
    def initUI(self):
        """初始化UI（现代深色主题）"""
        self.setWindowTitle("FOFA By: 2tina")
        self.setMinimumSize(1280, 800)
        
        # 应用现代样式
        self.setStyleSheet(UIStyle.getMainStyleSheet())
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建菜单栏
        self.createMenuBar()
        
        # 创建查询区域（卡片式）
        query_card = QWidget()
        query_card.setStyleSheet(f"""
            QWidget {{
                background-color: {UIStyle.BG_CARD};
                border-radius: {UIStyle.RADIUS_LARGE}px;
                padding: 15px;
            }}
        """)
        query_card_layout = QVBoxLayout(query_card)
        query_card_layout.setSpacing(12)
        query_card_layout.setContentsMargins(15, 15, 15, 15)
        
        self.createQueryArea()
        query_card_layout.addLayout(self.query_layout)
        
        main_layout.addWidget(query_card)
        
        # 创建Tab区域
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.closeTab)
        main_layout.addWidget(self.tab_widget)
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        # 设置状态栏样式
        self.statusBar.setStyleSheet(f"""
            QStatusBar {{
                background-color: rgba(42, 45, 58, 0.8);
                color: {UIStyle.TEXT_SECONDARY};
                border-top: 1px solid {UIStyle.BG_DIVIDER};
                padding: 8px;
            }}
        """)
    
    def createMenuBar(self):
        """创建菜单栏（现代风格）"""
        menubar = self.menuBar()
        
        # 项目菜单
        project_menu = menubar.addMenu("项目")
        
        open_action = QAction("打开项目", self)
        open_action.triggered.connect(self.openProject)
        project_menu.addAction(open_action)
        
        save_action = QAction("保存项目", self)
        save_action.triggered.connect(self.saveProject)
        project_menu.addAction(save_action)
        
        # 配置菜单
        config_menu = menubar.addMenu("配置")
        
        set_config_action = QAction("修改配置", self)
        set_config_action.triggered.connect(self.setConfig)
        config_menu.addAction(set_config_action)
        
        config_menu.addSeparator()
        
        # 主题切换
        theme_menu = config_menu.addMenu("主题")
        
        common_action = QAction("常用主题（深色）", self)
        common_action.triggered.connect(lambda: self.switchTheme(ThemeMode.COMMON))
        theme_menu.addAction(common_action)
        
        white_action = QAction("白色主题", self)
        white_action.triggered.connect(lambda: self.switchTheme(ThemeMode.WHITE))
        theme_menu.addAction(white_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        query_api_action = QAction("获取当前查询语句", self)
        query_api_action.triggered.connect(self.getQueryAPI)
        help_menu.addAction(query_api_action)
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)
    
    def createQueryArea(self):
        """创建查询区域"""
        # 使用垂直布局包装查询区域
        self.query_layout = QVBoxLayout()
        
        # 第一行：查询输入框和按钮
        first_row = QHBoxLayout()
        
        # 查询标签（统一对齐，使用按钮主题样式）
        query_label = StyledLabel("查询条件：")
        query_label.setMinimumWidth(90)
        query_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        first_row.addWidget(query_label)
        
        # 查询输入框（加长）
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("请输入查询条件")
        self.query_input.returnPressed.connect(self.queryAction)
        self.query_input.setMinimumWidth(500)  # 加长输入框
        first_row.addWidget(self.query_input, 3)  # 增加宽度比例
        
        # 查询按钮（使用现代风格按钮）
        self.search_btn = ModernButton("查询", self)
        self.search_btn.clicked.connect(self.queryAction)
        first_row.addWidget(self.search_btn)
        
        # 导出按钮（使用现代风格按钮）
        self.export_btn = ModernButton("导出", self)
        self.export_btn.clicked.connect(self.exportAction)
        first_row.addWidget(self.export_btn)
        
        # 全选按钮
        self.select_all_btn = ModernButton("全选", self)
        self.select_all_btn.clicked.connect(self.selectAllAction)
        first_row.addWidget(self.select_all_btn)
        
        self.query_layout.addLayout(first_row)
        
        # 第二行：复选框（放在查询输入框下面）
        second_row = QHBoxLayout()
        second_row.addWidget(QLabel(""))  # 占位，与查询标签对齐
        
        # 复选框容器
        checkbox_container = QHBoxLayout()
        
        self.check_honeypot = QCheckBox("排除干扰")
        checkbox_container.addWidget(self.check_honeypot)
        
        self.check_fid = QCheckBox("Fid")
        checkbox_container.addWidget(self.check_fid)
        
        self.check_os = QCheckBox("os")
        checkbox_container.addWidget(self.check_os)
        
        self.check_icp = QCheckBox("icp")
        checkbox_container.addWidget(self.check_icp)
        
        self.check_product = QCheckBox("产品指纹")
        checkbox_container.addWidget(self.check_product)
        
        self.check_cert_cn = QCheckBox("证书CN")
        checkbox_container.addWidget(self.check_cert_cn)
        
        self.check_cert_org = QCheckBox("证书Org")
        checkbox_container.addWidget(self.check_cert_org)
        
        self.check_last_update = QCheckBox("最近更新时间")
        checkbox_container.addWidget(self.check_last_update)
        
        self.check_is_all = QCheckBox("全部")
        checkbox_container.addWidget(self.check_is_all)
        
        checkbox_container.addStretch()  # 添加弹性空间，使复选框靠左对齐
        
        second_row.addLayout(checkbox_container, 3)  # 与输入框对齐
        self.query_layout.addLayout(second_row)
    
    def initHomePage(self):
        """初始化首页"""
        home_tab = QWidget()
        layout = QVBoxLayout(home_tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 证书查询区域
        cert_group = QGroupBox("计算证书序列号")
        cert_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_LARGE}px;
                margin-top: 10px;
                padding-top: 15px;
                font-size: 14px;
                color: {UIStyle.TEXT_PRIMARY};
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
        """)
        cert_layout = QHBoxLayout()
        cert_layout.setSpacing(12)
        cert_layout.setContentsMargins(0, 0, 0, 0)
        # 使用样式化标签（按钮主题样式，但不可点击）
        cert_label = StyledLabel("证书序列号：")
        cert_label.setMinimumWidth(110)  # 统一标签宽度，确保对齐
        cert_label.setMaximumWidth(110)
        cert_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        cert_input = QLineEdit()
        cert_input.setPlaceholderText("请输入16进制证书序列号")
        cert_btn = ModernButton("计算并查询", self)
        cert_btn.clicked.connect(lambda: self.queryCert(cert_input.text().strip()))
        cert_layout.addWidget(cert_label)
        cert_layout.addWidget(cert_input, 5)  # 增加输入框宽度比例
        cert_layout.addWidget(cert_btn)
        cert_group.setLayout(cert_layout)
        layout.addWidget(cert_group)
        
        # Favicon查询区域
        favicon_group = QGroupBox("计算Favicon Hash")
        favicon_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {UIStyle.BG_CARD};
                border: 2px solid {UIStyle.BG_DIVIDER};
                border-radius: {UIStyle.RADIUS_LARGE}px;
                margin-top: 10px;
                padding-top: 15px;
                font-size: 14px;
                color: {UIStyle.TEXT_PRIMARY};
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "PingFang SC", "Segoe UI", sans-serif;
            }}
        """)
        favicon_layout = QHBoxLayout()
        favicon_layout.setSpacing(12)
        favicon_layout.setContentsMargins(0, 0, 0, 0)
        # 使用样式化标签（按钮主题样式，但不可点击）
        favicon_label = StyledLabel("Favicon URL：")
        favicon_label.setMinimumWidth(110)  # 与证书序列号标签宽度一致
        favicon_label.setMaximumWidth(110)
        favicon_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        favicon_input = QLineEdit()
        favicon_input.setPlaceholderText("请输入Favicon URL或拖拽文件")
        favicon_btn = ModernButton("计算并查询", self)
        favicon_btn.clicked.connect(lambda: self.queryFavicon(favicon_input.text().strip()))
        favicon_layout.addWidget(favicon_label)
        favicon_layout.addWidget(favicon_input, 5)  # 增加输入框宽度比例
        favicon_layout.addWidget(favicon_btn)
        favicon_group.setLayout(favicon_layout)
        layout.addWidget(favicon_group)
        
        # 命令指南（可滚动）
        command_guide = CommandGuide(self)
        command_guide.command_clicked.connect(self.onCommandClicked)
        layout.addWidget(command_guide, 1)  # 占据剩余空间
        
        self.tab_widget.addTab(home_tab, "首页")
    
    def onCommandClicked(self, command: str):
        """命令指南点击事件"""
        # 将命令填充到查询条件输入框
        self.query_input.setText(command)
        self.query_input.setFocus()
    
    def queryAction(self):
        """查询操作"""
        from utils.security import SecurityUtil
        
        query_text = self.query_input.text().strip()
        if not query_text:
            QMessageBox.warning(self, "警告", "请输入查询条件")
            return
        
        # 安全验证
        query_text = SecurityUtil.sanitize_query(query_text)
        
        self.query([query_text])
    
    def query(self, query_list: List[str]):
        """执行查询"""
        for query_text in query_list:
            query_text = query_text.strip()
            if not query_text:
                continue
            
            tab_title = query_text
            
            # 处理排除干扰选项
            if self.check_honeypot.isChecked():
                if not query_text.startswith("(*)"):
                    tab_title = f"(*){query_text}"
                    query_text = f"({query_text}) && (is_honeypot=false && is_fraud=false)"
            
            # 检查Tab是否已存在
            if self.isTabExists(tab_title):
                self.tab_widget.setCurrentIndex(self.getTabIndex(tab_title))
                continue
            
            # 设置额外字段
            additional_fields = []
            if self.check_fid.isChecked():
                additional_fields.append("fid")
            if self.check_os.isChecked():
                additional_fields.append("os")
            if self.check_icp.isChecked():
                additional_fields.append("icp")
            if self.check_product.isChecked():
                additional_fields.append("product")
            if self.check_cert_cn.isChecked():
                additional_fields.append("certs_subject_cn")
            if self.check_cert_org.isChecked():
                additional_fields.append("certs_subject_org")
            if self.check_last_update.isChecked():
                additional_fields.append("lastupdatetime")
            
            self.config.additionalField = additional_fields
            
            # 创建查询URL
            encoded_query = self.request_util.encode(query_text)
            url = self.config.getParam(self.check_is_all.isChecked()) + encoded_query
            
            # 创建Tab和数据Bean
            tab = self.createResultTab(tab_title)
            tab_data = TabDataBean()
            self.tab_data[tab_title] = tab_data
            
            # 执行查询
            self.executeQuery(url, tab, tab_data, tab_title)
    
    def createResultTab(self, title: str) -> QWidget:
        """创建结果Tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建表格
        table = QTableWidget()
        table.setColumnCount(8 + len(self.config.additionalField))
        headers = ["序号", "HOST", "标题", "IP", "端口", "域名", "协议", "Server"]
        headers.extend(self.config.additionalField)
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # 改为单选
        table.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)  # 禁用右键菜单
        table.setAlternatingRowColors(False)  # 不交替显示颜色，只显示一个颜色
        table.horizontalHeader().setStretchLastSection(True)
        table.setSortingEnabled(True)
        
        # 隐藏行号（verticalHeader），避免左侧乱码
        table.verticalHeader().setVisible(False)
        
        # 设置表格字体，确保中文正确显示（使用UTF-8编码）
        font = table.font()
        # 优先使用支持中文的字体
        font.setFamily("Microsoft YaHei UI, Microsoft YaHei, SimHei, PingFang SC, Segoe UI, Arial, sans-serif")
        font.setPixelSize(13)  # 使用像素大小，避免DPI缩放问题
        font.setStyleHint(font.StyleHint.SansSerif)  # 确保使用无衬线字体
        font.setHintingPreference(font.HintingPreference.PreferDefaultHinting)
        table.setFont(font)
        
        # 设置表头字体，确保中文正确显示
        header_font = table.horizontalHeader().font()
        header_font.setFamily("Microsoft YaHei UI, Microsoft YaHei, SimHei, PingFang SC, Segoe UI, Arial, sans-serif")
        header_font.setPixelSize(13)
        header_font.setBold(True)
        table.horizontalHeader().setFont(header_font)
        
        # 设置序号列对齐方式和宽度
        table.setColumnWidth(0, 70)  # 序号列固定宽度
        table.setColumnWidth(1, 200)  # HOST列
        table.setColumnWidth(2, 200)  # 标题列
        table.setColumnWidth(3, 120)  # IP列
        table.setColumnWidth(4, 60)   # 端口列
        table.setColumnWidth(5, 180)  # 域名列
        table.setColumnWidth(6, 80)   # 协议列
        table.setColumnWidth(7, 120)  # Server列
        
        # 确保表格使用UTF-8编码
        table.setProperty("encoding", "UTF-8")
        
        # 只保留双击访问URL功能
        table.itemDoubleClicked.connect(lambda item: self.openUrlFromTable(table, item.row()))
        
        # 设置表格样式（现代深色主题）
        table.setStyleSheet(f"""
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
        """)
        
        layout.addWidget(table)
        
        # 添加Tab
        self.tab_widget.addTab(tab, title)
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
        
        return tab
    
    def executeQuery(self, url: str, tab: QWidget, tab_data: TabDataBean, tab_title: str):
        """执行查询"""
        # 显示加载状态
        table = tab.findChild(QTableWidget)
        if table:
            table.setRowCount(1)
            table.setItem(0, 0, QTableWidgetItem("正在查询..."))
        
        # 创建查询线程
        thread = QueryThread(url, self)
        
        # 连接信号
        def on_finished(result):
            self.onQueryFinished(result, tab, tab_data, tab_title)
            if thread in self.threads:
                self.threads.remove(thread)
        
        def on_error(error):
            self.onQueryError(error, tab)
            if thread in self.threads:
                self.threads.remove(thread)
        
        thread.finished.connect(on_finished)
        thread.error.connect(on_error)
        self.threads.append(thread)
        thread.start()
    
    def onQueryFinished(self, result: Dict, tab: QWidget, tab_data: TabDataBean, tab_title: str):
        """查询完成回调（确保在主线程执行）"""
        # 确保在主线程执行UI更新
        app = QApplication.instance()
        if app and app.thread() != QThread.currentThread():
            QTimer.singleShot(0, lambda: self.onQueryFinished(result, tab, tab_data, tab_title))
            return
        
        table = tab.findChild(QTableWidget)
        if not table:
            return
        
        if result.get("code") == "200":
            try:
                obj = json.loads(result["msg"])
                if obj.get("error"):
                    QMessageBox.warning(self, "错误", obj.get("errmsg", "查询失败"))
                    return
                
                # 加载数据（在后台线程执行）
                data_list = DataUtil.loadJsonData(tab_data, obj, None, None, False)
                
                # 分批更新表格，避免UI冻结
                self.updateTableAsync(table, data_list)
                
                # 更新状态
                tab_data.total = obj.get("size", 0)
                if obj.get("next"):
                    tab_data.next = obj["next"]
                if tab_data.total < int(self.config.size):
                    tab_data.hasMoreData = False
                
                # 更新状态栏
                self.statusBar.showMessage(f"查询成功: {tab_data.total} 条结果")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"解析数据失败: {str(e)}")
        else:
            QMessageBox.warning(self, "错误", result.get("msg", "查询失败"))
    
    def onQueryError(self, error: str, tab: QWidget):
        """查询错误回调（确保在主线程执行）"""
        # 确保在主线程执行UI更新
        app = QApplication.instance()
        if app and app.thread() != QThread.currentThread():
            QTimer.singleShot(0, lambda: self.onQueryError(error, tab))
            return
        
        table = tab.findChild(QTableWidget)
        if table:
            table.setRowCount(1)
            table.setItem(0, 0, QTableWidgetItem(f"查询失败: {error}"))
        
        self.statusBar.showMessage(f"查询失败: {error}")
    
    def updateTableAsync(self, table: QTableWidget, data_list: List[TableBean]):
        """异步更新表格（分批更新避免UI冻结）"""
        if not data_list:
            table.setRowCount(0)
            return
        
        # 禁用排序以提高性能
        table.setSortingEnabled(False)
        
        # 设置行数
        table.setRowCount(len(data_list))
        
        # 分批更新，每批50行
        batch_size = 50
        current_row = [0]  # 使用列表以在闭包中修改
        
        def updateBatch():
            """更新一批数据"""
            start = current_row[0]
            end = min(start + batch_size, len(data_list))
            
            for row in range(start, end):
                data = data_list[row]
                if row >= table.rowCount():
                    table.insertRow(row)
                
                # 序号列：确保使用正确的字体和编码，避免乱码
                num_str = str(data.num) if data.num else "0"
                num_item = QTableWidgetItem(num_str)
                # 使用支持中文的字体，确保数字正确显示
                num_font = table.font()
                num_font.setFamily("Microsoft YaHei UI, Microsoft YaHei, SimHei, Arial, sans-serif")
                num_font.setPixelSize(13)
                num_font.setStyleHint(num_font.StyleHint.SansSerif)
                num_font.setHintingPreference(num_font.HintingPreference.PreferDefaultHinting)
                num_item.setFont(num_font)
                num_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                table.setItem(row, 0, num_item)
                
                # 确保所有文本使用正确字体，避免中文乱码
                # 获取表格字体（已设置为支持中文的字体）
                cell_font = table.font()
                
                host_item = QTableWidgetItem(data.host if data.host else "")
                host_item.setFont(cell_font)
                table.setItem(row, 1, host_item)
                
                title_item = QTableWidgetItem(data.title if data.title else "")
                title_item.setFont(cell_font)
                table.setItem(row, 2, title_item)
                
                ip_item = QTableWidgetItem(data.ip if data.ip else "")
                ip_item.setFont(cell_font)
                table.setItem(row, 3, ip_item)
                
                port_str = str(data.port) if data.port else ""
                port_item = QTableWidgetItem(port_str)
                port_item.setFont(cell_font)
                table.setItem(row, 4, port_item)
                
                domain_item = QTableWidgetItem(data.domain if data.domain else "")
                domain_item.setFont(cell_font)
                table.setItem(row, 5, domain_item)
                
                protocol_item = QTableWidgetItem(data.protocol if data.protocol else "")
                protocol_item.setFont(cell_font)
                table.setItem(row, 6, protocol_item)
                
                server_item = QTableWidgetItem(data.server if data.server else "")
                server_item.setFont(cell_font)
                table.setItem(row, 7, server_item)
                
                # 确保所有额外字段也使用正确字体
                cell_font = table.font()
                
                col = 8
                if "fid" in self.config.additionalField:
                    fid_item = QTableWidgetItem(data.fid if data.fid else "")
                    fid_item.setFont(cell_font)
                    table.setItem(row, col, fid_item)
                    col += 1
                if "os" in self.config.additionalField:
                    os_item = QTableWidgetItem(data.os if data.os else "")
                    os_item.setFont(cell_font)
                    table.setItem(row, col, os_item)
                    col += 1
                if "icp" in self.config.additionalField:
                    icp_item = QTableWidgetItem(data.icp if data.icp else "")
                    icp_item.setFont(cell_font)
                    table.setItem(row, col, icp_item)
                    col += 1
                if "product" in self.config.additionalField:
                    product_item = QTableWidgetItem(data.product if data.product else "")
                    product_item.setFont(cell_font)
                    table.setItem(row, col, product_item)
                    col += 1
                if "certs_subject_cn" in self.config.additionalField:
                    cert_cn_item = QTableWidgetItem(data.certCN if data.certCN else "")
                    cert_cn_item.setFont(cell_font)
                    table.setItem(row, col, cert_cn_item)
                    col += 1
                if "certs_subject_org" in self.config.additionalField:
                    cert_org_item = QTableWidgetItem(data.certOrg if data.certOrg else "")
                    cert_org_item.setFont(cell_font)
                    table.setItem(row, col, cert_org_item)
                    col += 1
                if "lastupdatetime" in self.config.additionalField:
                    lastupdate_item = QTableWidgetItem(data.lastupdatetime if data.lastupdatetime else "")
                    lastupdate_item.setFont(cell_font)
                    table.setItem(row, col, lastupdate_item)
                    col += 1
            
            current_row[0] = end
            
            # 如果还有数据，继续更新下一批
            if end < len(data_list):
                QTimer.singleShot(10, updateBatch)  # 10ms后更新下一批
            else:
                # 所有数据更新完成，重新启用排序
                table.setSortingEnabled(True)
        
        # 开始更新
        updateBatch()
    
    def isTabExists(self, title: str) -> bool:
        """检查Tab是否存在"""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == title:
                return True
        return False
    
    def getTabIndex(self, title: str) -> int:
        """获取Tab索引"""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == title:
                return i
        return -1
    
    def closeTab(self, index: int):
        """关闭Tab"""
        if index > 0:  # 保留首页
            title = self.tab_widget.tabText(index)
            self.tab_widget.removeTab(index)
            if title in self.tab_data:
                del self.tab_data[title]
    
    def openUrlFromTable(self, table: QTableWidget, row: int):
        """从表格行打开URL（双击事件）"""
        if row < 0 or row >= table.rowCount():
            return
        
        # 获取host和protocol
        host_item = table.item(row, 1)
        protocol_item = table.item(row, 6)
        
        if not host_item:
            return
        
        host = host_item.text()
        protocol = protocol_item.text() if protocol_item else ""
        
        # 构建URL
        if not host.startswith("http"):
            if protocol.lower() == "https" or ":443" in host:
                url = f"https://{host}"
            else:
                url = f"http://{host}"
        else:
            url = host
        
        # 移除端口号
        if ":443" in url:
            url = url.replace(":443", "")
        elif ":80" in url:
            url = url.replace(":80", "")
        
        # 打开浏览器
        try:
            QDesktopServices.openUrl(QUrl(url))
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法打开URL: {str(e)}")
    
    def queryCert(self, cert_text: str):
        """查询证书"""
        if not cert_text:
            QMessageBox.warning(self, "警告", "请输入证书序列号")
            return
        
        # 清理输入：移除所有空格、制表符、换行符等空白字符
        cert_text = ''.join(cert_text.split())
        
        if not cert_text:
            QMessageBox.warning(self, "错误", "证书序列号不能为空")
            return
        
        try:
            # 验证是否为有效的16进制字符串
            if not all(c in '0123456789ABCDEFabcdef' for c in cert_text):
                QMessageBox.warning(self, "错误", "证书序列号必须为16进制数字")
                return
            
            # 转换为整数
            cert_num = int(cert_text, 16)
            self.query([f'cert="{cert_num}"'])
        except ValueError as e:
            QMessageBox.warning(self, "错误", f"无效的证书序列号: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理证书序列号时出错: {str(e)}")
    
    def queryFavicon(self, url: str):
        """查询Favicon"""
        if not url:
            QMessageBox.warning(self, "警告", "请输入Favicon URL")
            return
        
        # 清理输入：移除前后空格
        url = url.strip()
        
        if not url:
            QMessageBox.warning(self, "错误", "Favicon URL不能为空")
            return
        
        # 在后台线程执行网络请求
        class FaviconQueryThread(QThread):
            finished = Signal(dict)
            error_signal = Signal(str)
            
            def __init__(self, url, request_util):
                super().__init__()
                self.url = url
                self.request_util = request_util
            
            def run(self):
                try:
                    # 获取favicon链接
                    link = self.request_util.getLinkIcon(self.url)
                    if link:
                        res = self.request_util.getImageFavicon(link)
                    else:
                        res = self.request_util.getImageFavicon(self.url + "/favicon.ico")
                    
                    if res:
                        self.finished.emit(res)
                    else:
                        self.error_signal.emit("无法获取Favicon")
                except Exception as e:
                    self.error_signal.emit(str(e))
        
        thread = FaviconQueryThread(url, self.request_util)
        thread.finished.connect(lambda res: self.onFaviconQueryFinished(res))
        thread.error_signal.connect(lambda err: QMessageBox.warning(self, "错误", f"查询Favicon失败: {err}"))
        thread.start()
    
    def onFaviconQueryFinished(self, res: Dict):
        """Favicon查询完成回调"""
        if res and res.get("code") == "200":
            self.query([res.get("msg")])
        else:
            QMessageBox.warning(self, "错误", "无法获取Favicon Hash")
    
    def exportAction(self):
        """导出操作"""
        from utils.security import SecurityUtil
        
        current_index = self.tab_widget.currentIndex()
        if current_index == 0:  # 首页
            QMessageBox.warning(self, "警告", "首页无数据可导出")
            return
        
        # 选择导出格式
        format_dialog = QMessageBox(self)
        format_dialog.setWindowTitle("选择导出格式")
        format_dialog.setText("请选择导出格式：")
        excel_btn = format_dialog.addButton("Excel", QMessageBox.ButtonRole.AcceptRole)
        txt_btn = format_dialog.addButton("TXT", QMessageBox.ButtonRole.AcceptRole)
        cancel_btn = format_dialog.addButton("取消", QMessageBox.ButtonRole.RejectRole)
        format_dialog.exec()
        
        export_format = None
        if format_dialog.clickedButton() == excel_btn:
            export_format = "excel"
        elif format_dialog.clickedButton() == txt_btn:
            export_format = "txt"
        else:
            return
        
        # 选择保存目录
        dir_path = QFileDialog.getExistingDirectory(self, "选择导出目录")
        if not dir_path:
            return
        
        # 验证路径安全
        safe_path_obj = SecurityUtil.safe_path(dir_path)
        if not safe_path_obj:
            QMessageBox.warning(self, "警告", "无效的导出路径")
            return
        
        # 获取当前Tab数据
        tab_title = self.tab_widget.tabText(current_index)
        tab_data = self.tab_data.get(tab_title)
        
        if not tab_data:
            QMessageBox.warning(self, "警告", "无数据可导出")
            return
        
        # 获取表格数据
        tab = self.tab_widget.widget(current_index)
        table = tab.findChild(QTableWidget)
        if not table:
            QMessageBox.warning(self, "警告", "无法获取表格数据")
            return
        
        # 准备导出数据
        total_data = []
        urls = []
        
        for row in range(table.rowCount()):
            if table.item(row, 1) is None:
                continue
            
            excel_bean = ExcelBean()
            excel_bean.host = table.item(row, 1).text()
            excel_bean.title = table.item(row, 2).text() if table.item(row, 2) else ""
            excel_bean.ip = table.item(row, 3).text()
            excel_bean.port = int(table.item(row, 4).text()) if table.item(row, 4) else 0
            excel_bean.domain = table.item(row, 5).text() if table.item(row, 5) else ""
            excel_bean.protocol = table.item(row, 6).text() if table.item(row, 6) else ""
            excel_bean.server = table.item(row, 7).text() if table.item(row, 7) else ""
            
            total_data.append(excel_bean)
            
            # 准备URL（用于TXT导出）
            host = excel_bean.host
            protocol = excel_bean.protocol.lower()
            if not host.startswith("http"):
                if protocol == "https" or excel_bean.port == 443:
                    url = f"https://{host}"
                else:
                    url = f"http://{host}"
            else:
                url = host
            urls.append(url)
        
        # 生成文件名
        import time
        if export_format == "excel":
            safe_filename = SecurityUtil.sanitize_filename(f"fofa导出结果_{int(time.time())}.xlsx")
            file_path = safe_path_obj / safe_filename
            
            # 导出Excel
            success, message = DataUtil.exportToExcel(
                str(file_path),
                tab_title,
                total_data,
                [[url] for url in urls],
                ""
            )
        else:
            # 导出TXT
            safe_filename = SecurityUtil.sanitize_filename(f"fofa导出结果_{int(time.time())}.txt")
            file_path = safe_path_obj / safe_filename
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for url in urls:
                        f.write(url + '\n')
                success = True
                message = f"导出成功！文件保存在 {file_path}"
            except Exception as e:
                success = False
                message = f"导出失败：{str(e)}"
        
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.warning(self, "失败", message)
    
    def openProject(self):
        """打开项目"""
        file_path, _ = QFileDialog.getOpenFileName(self, "打开项目", "", "文本文件 (*.txt)")
        if file_path:
            # TODO: 实现打开项目
            pass
    
    def saveProject(self):
        """保存项目"""
        # TODO: 实现保存项目
        pass
    
    def setConfig(self):
        """设置配置"""
        from controllers.config_dialog import ConfigDialog
        dialog = ConfigDialog(self)
        if dialog.exec():
            # 重新加载配置
            DataUtil.loadConfigure()
    
    def getQueryAPI(self):
        """获取当前查询语句"""
        from PySide6.QtGui import QClipboard
        
        current_index = self.tab_widget.currentIndex()
        if current_index == 0:
            QMessageBox.information(self, "提示", "首页无查询语句")
            return
        
        title = self.tab_widget.tabText(current_index)
        # 获取查询语句
        query_text = DataUtil.replaceString(title)
        
        # 复制查询语句到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(query_text)
        QMessageBox.information(self, "查询语句", f"查询语句已复制到剪贴板:\n{query_text}")
    
    def showAbout(self):
        """显示关于"""
        QMessageBox.about(self, "关于", "FOFA By: 2tina\n\n基于FOFA API的查询工具")
    
    def selectAllAction(self):
        """全选操作"""
        current_index = self.tab_widget.currentIndex()
        if current_index == 0:  # 首页
            return
        
        tab = self.tab_widget.widget(current_index)
        table = tab.findChild(QTableWidget)
        if table:
            table.selectAll()
    
    def copyToClipboard(self, text: str):
        """复制到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "提示", "已复制到剪贴板")
    
    def queryFaviconFromHost(self, host: str, protocol: str):
        """从host查询favicon（在后台线程执行）"""
        if not host:
            return
        
        # 构建URL
        if not host.startswith("http"):
            if protocol == "https" or ":443" in host:
                url = f"https://{host}"
            else:
                url = f"http://{host}"
        else:
            url = host
        
        # 移除端口号
        if ":443" in url:
            url = url.replace(":443", "")
        elif ":80" in url:
            url = url.replace(":80", "")
        
        # 在后台线程执行网络请求
        class FaviconThread(QThread):
            finished = Signal(dict)
            
            def __init__(self, url, request_util):
                super().__init__()
                self.url = url
                self.request_util = request_util
            
            def run(self):
                link = self.request_util.getLinkIcon(self.url)
                if link:
                    res = self.request_util.getImageFavicon(link)
                else:
                    res = self.request_util.getImageFavicon(self.url + "/favicon.ico")
                self.finished.emit(res)
        
        thread = FaviconThread(url, self.request_util)
        thread.finished.connect(lambda res: self.onFaviconQueryFinished(res))
        thread.start()
    
    def onFaviconQueryFinished(self, res: Dict):
        """Favicon查询完成回调"""
        if res and res.get("code") == "200":
            self.query([res.get("msg")])
        else:
            QMessageBox.warning(self, "错误", "无法获取favicon")
    
    def queryCertFromHost(self, host: str):
        """从host查询证书序列号（在后台线程执行）"""
        if not host:
            return
        
        # 移除协议前缀和端口号
        clean_host = host.replace("http://", "").replace("https://", "")
        if ":443" in clean_host:
            clean_host = clean_host.replace(":443", "")
        elif ":80" in clean_host:
            clean_host = clean_host.replace(":80", "")
        
        # 在后台线程执行网络请求
        class CertThread(QThread):
            finished = Signal(str)
            
            def __init__(self, host, request_util):
                super().__init__()
                self.host = host
                self.request_util = request_util
            
            def run(self):
                cert_query = self.request_util.getCertSerialNum(self.host)
                self.finished.emit(cert_query if cert_query else "")
        
        thread = CertThread(clean_host, self.request_util)
        thread.finished.connect(lambda cert: self.onCertQueryFinished(cert))
        thread.start()
    
    def onCertQueryFinished(self, cert_query: str):
        """证书查询完成回调"""
        if cert_query:
            self.query([cert_query])
        else:
            QMessageBox.warning(self, "错误", "无法获取证书序列号")
    
    def switchTheme(self, mode: ThemeMode):
        """切换主题"""
        self.theme_manager.setMode(mode)
        self.applyTheme()
    
    def applyTheme(self):
        """应用主题"""
        # 应用主题管理器
        self.theme_manager.applyTheme(self)
        
        # 应用样式表（会根据主题更新）
        self.setStyleSheet(UIStyle.getMainStyleSheet())
        
        # 更新所有子组件
        for widget in self.findChildren(QWidget):
            if isinstance(widget, ModernButton):
                if hasattr(widget, 'updateStyle'):
                    widget.updateStyle()
        
        # 更新所有表格样式
        for table in self.findChildren(QTableWidget):
            colors = self.theme_manager.getColors()
            table.setStyleSheet(f"""
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
            """)
        
        self.update()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 等待所有线程完成
        if self.threads:
            for thread in self.threads[:]:  # 复制列表避免迭代时修改
                if thread.isRunning():
                    thread.quit()
                    thread.wait(3000)  # 等待最多3秒
                    if thread.isRunning():
                        thread.terminate()
                        thread.wait(1000)
        
        # 调用父类关闭事件
        super().closeEvent(event)

