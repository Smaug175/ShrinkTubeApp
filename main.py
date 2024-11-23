import json
import os

# 主界面缩放因子
os.environ['QT_SCALE_FACTOR'] = '1.5'

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication, QMainWindow, QTableWidget, \
    QTableWidgetItem, QVBoxLayout, QWidget, QTabWidget, QLabel, QComboBox, \
    QAction, QPushButton, QHBoxLayout, QToolBar, QLineEdit, QFrame, QTextEdit, \
    QSizePolicy, QAbstractItemView, QDialog

from bin.utils.AutoLogger import AutoLoggerClass
from bin.ShrinkTube import ShrinkTubeClass
from bin.utils.CryptoData import CryptoDataClass
from bin.utils.ConfigSetting import ConfigSettingClass
from bin.UI.ReserachResult import ReserachResultDialog, ReserachResultDialog_Mold
from bin.UI.Config import ConfigResultDialog
from bin.UI.Config import ModifyConfigResultDialog
from bin.UI.Selection_Mold import ComboCheckBox
from bin.UI.Login import LoginWindow
from bin.utils.Authorization import AuthorizationClass


def screen_size():
    """获取屏幕尺寸"""
    screen = QApplication.desktop().screenGeometry()
    return screen.width(), screen.height()


class AppUiDemo(QMainWindow):
    """程序运行的主界面

    Methods
    _______1
    __init__(self)
        验证许可及账户登录
    initUI(self)
        初始化程序主界面
    Normal(self)
        普通抽界面初始化功能
    normal_import_file(self)
        导入管件的DXF文件
    normal_calculate(self)
        计算模具参数
    save_params_to_db(self)
        保存模具参数
    normal_export_file(self)
        导出模具的DXF文件
    """

    def __init__(self):
        """验证许可及账户登录

        许可认证不成功，将弹出提示框，提示用户认证失败，并结束程序运行。
        """

        super().__init__()

        self.version = '0.2.3'

        # 初始界面的HTML文本
        self.init_html_text = """
                <html>
                <head>
                <style>
                  body { font-family: Arial, sans-serif; }
                  h1 { font-size: 24px; color: black; }
                  h2 { font-size: 24px; color: black; }
                  p { font-size: 24px; color: black; }
                </style>
                </head>
                <body>
                <h1>首先阅读! 该软件各部分功能如下：</h1>
                <hr>
                <h1>一、普通抽</h1>
                <p>普通抽可选择是否需要额外的壁厚，可选择需要操作的模具。</p>
                <hr>
                <h1>二、TP抽</h1>
                <p>TP抽还未完善。</p>
                <hr>
                <h1>三、数据库管理</h1>
                <h2>1. 显示所有数据</h2>
                <p>该功能将显示所有的抽管记录。以车种规格作为唯一值，不可重复。</p>
                <p>项目页下包含管件参数以及不同模具的参数，不可在此修改参数值。</p>
                <h2>2. 显示模具数据</h2>
                <p>该功能将显示所有的模具的图号及参数。其中，车种规格作为唯一值，与图号绑定，不可重复。</p>
                <p>图号的编码方式是在最大图号的基础上加一。不同模具不共用图号编码。</p>
                <h2>3. 搜索车种规格</h2>
                <p>该功能基于车种规格的名称，从数据库中搜索含有该车种规格的项目。若存在，则显示整个项目。</p>
                <h2>4. 删除车种规格</h2>
                <p>该功能基于车种规格的名称，从数据库中删除含有该车种规格的项目。若存在，则首先显示整个项目，随后确认是否删除。（删除需要谨慎）</p>
                <h2>5. 搜索图号</h2>
                <p>该功能基于图号，从数据库中搜索该图号的模具。若存在，则显示当前模具参数。</p>
                <h2>6. 删除图号</h2>
                <p>该功能基于图号，从数据库中删除含有该图号的模具。若存在，则首先显示模具参数，随后确认是否删除。（删除需要谨慎）</p>
                <p>删除模具时，会将该模具的图号从数据库中删除，但不会车种规格所属的项目。</p>
                </body>
                </html>
                """

        # 编写HTML格式的文本，包括样式和层级
        self.normal_html_text = """
                <html>
                <head>
                <style>
                  body { font-family: Arial, sans-serif; }
                  h1 { font-size: 24px; color: black; }
                  h2 { font-size: 24px; color: black; }
                  p { font-size: 24px; color: black; }
                  table { width: 100%; border-collapse: collapse; font-size: 24px; color: black; }
                </style>
                </head>
                <body>
                <h1>首先阅读! 普通抽的各部分功能如下：</h1>
                <hr>
                <h1>一、导入管件的DXF文件</h1>
                <p>导入管件的文件必须有必要的参数描述，参数描述使用标准规则。标准规则见示例视频。同时需要将“车种规格”在输入图中额外注明。不同壁厚管件所需参数表如下。</p>
                <center>
                <table border="1" style="margin-left: auto; margin-right: auto;">
                  <caption>不同壁厚所需参数表</caption>
                  <thead>
                    <tr>
                      <th style="text-align: center;">两段不同壁厚</th>
                      <th style="text-align: center;">三段不同壁厚</th>
                      <th style="text-align: center;">描述</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td style="text-align: center;">车种规格</td>
                      <td style="text-align: center;">车种规格</td>
                      <td style="text-align: center;">当前管件所属车种规格</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;">D</td>
                      <td style="text-align: center;">D</td>
                      <td style="text-align: center;">抽管外径</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;">L</td>
                      <td style="text-align: center;">L</td>
                      <td style="text-align: center;">抽管总长</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;">L1</td>
                      <td style="text-align: center;">L1</td>
                      <td style="text-align: center;">壁厚从厚开始，第一段长度</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;">T1</td>
                      <td style="text-align: center;">T1</td>
                      <td style="text-align: center;">第一段壁厚</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;">M1</td>
                      <td style="text-align: center;">M1</td>
                      <td style="text-align: center;">第一段过渡段长度</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;">L2</td>
                      <td style="text-align: center;">L2</td>
                      <td style="text-align: center;">壁厚从厚开始，第二段长度</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;"></td>
                      <td style="text-align: center;">T2</td>
                      <td style="text-align: center;">第二段壁厚</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;"></td>
                      <td style="text-align: center;">M2</td>
                      <td style="text-align: center;">第二段过渡段长度</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;"></td>
                      <td style="text-align: center;">L3</td>
                      <td style="text-align: center;">壁厚从厚开始，第三段长度</td>
                    </tr>
                    <tr>
                      <td style="text-align: center;"></td>
                      <td style="text-align: center;">T3</td>
                      <td style="text-align: center;">第三段壁厚</td>
                    </tr>
                  </tbody>
                </table>
                </center>
                <hr>
                <h1>二、计算模具参数</h1>
                <p>需要选择输出模具的机器类型，默认选择DC0124。</p>
                <p>可选择是否增加额外壁厚，默认否。增加额外壁厚会自动加入成型模具。</p>
                <p>默认全选可计算的模具，可选择需要计算的模具。</p>
                <p>模具参数将会依照规则自动计算。可在此修改表格参数内容。</p>
                <hr>
                <h1>三、保存模具参数</h1>
                <h2>1. 新车种规格</h2>
                <p>数据将一键保存。</p>
                <h2>2. 已存在该车种规格</h2>
                <p>若没有模具，则会自动保存。</p>
                <p>若已经有模具，则会提示是否覆盖保存。</p>
                <hr>
                <h1>四、导出模具的DXF文件</h1>
                <h2>1. 自定义保存位置</h2>
                <p>选择路径文件夹，将在该路径下生成车架规格命名的文件夹（若存在，则命名后缀 + 1）。文件夹内含有模具的DXF图和Excel参数表格。模具使用该模具的图号命名。</p>
                <h2>2. 默认保存位置</h2>
                <p>默认保存位置位于程序根目录下的output文件夹内，将在该路径下生成车架规格命名的文件夹（若存在，则命名后缀 + 1）。文件夹内含有模具的DXF图和Excel参数表格。模具使用该模具的图号命名。</p>
                </body>
                </html>
                """

        self.logger = AutoLoggerClass()
        self.logger.info("程序开始运行")

        # 许可认证
        try:
            authorization_instance = AuthorizationClass(self.logger)
            self.message, self.pass_ = authorization_instance.get_message_and_pass()
            # self.message : str; 含有认证信息的具体内容。
            # self.pass_ : bool; 是否认证通过，True为通过，False为不通过。
        
            if not self.pass_:
                QMessageBox.information(self, "许可认证失败",
                                        self.message + '\n获取License请联系：smaugfire@163.com\n程序结束运行')
                print('许可认证失败！\n原因：'+self.message)
        
                self.logger.error("License验证失败！")
                self.logger.info("程序结束运行")
                self.logger.close()
                sys.exit()
            else:
                QMessageBox.information(self, "程序认证成功", "License 及 Mac Address 认证成功！")
        except Exception as e:
            temp_str = ('程序认证失败！错误位置：\n'
                        'AppUiDemo -> __init__ -> authorization_instance = AuthorizationClass(self.logger)\n'
                        '报错信息：')+str(e)
            QMessageBox.information(self, "程序认证失败", temp_str)
            print(temp_str)
        
            self.logger.error("程序认证失败！\n报错信息：{}".format(e))
            self.logger.info("程序结束运行")
            self.logger.close()
            sys.exit()
        #
        # 登录窗口
        try:
            self.login_window = LoginWindow(self, self.logger)
            # 弹出登录窗口并等待用户操作
            self.login_window.exec_()
        except Exception as e:
            temp_str = ('登录失败！错误位置：\n'
                        'AppUiDemo -> __init__ -> self.login_window = LoginWindow(self, self.logger)\n'
                        '报错信息：')+str(e)
            QMessageBox.information(self, "登录失败", temp_str)
            print(temp_str)

            self.logger.error("登录失败！报错信息：{}".format(e))
            self.logger.info("程序结束运行")
            self.logger.close()
            sys.exit()

        # 获取用户信息
        if self.login_window.result() == QDialog.Accepted:
            self.ID, self.user_name = self.login_window.get_ID_name()
            # self.ID : str; 用户ID
            # self.user_name : str; 用户名，用于后续计算时记录操作者。
        else:
            self.logger.info("用户未登录，程序结束运行")
            self.logger.close()
            sys.exit()

        # 抽管实例，用于计算和出图
        self.shrink_tube_instance = None

        # 加密数据的实例
        self.crypto_data_instance = CryptoDataClass(self.logger)

        # 配置文件的路径，初始化为默认配置文件
        self.config_path = 'config/default.json'

        # 配置设置的实例
        self.config_setting_instance = ConfigSettingClass(self.logger, self.config_path)

        # 从配置实例中获取所有配置数据
        self.config = self.config_setting_instance.get_all_config()

        self.logger.info("加载默认配置文件成功！，路径为：{}".format(self.config_path))

        # 初始化程序主界面
        self.initUI()

    def initUI(self):
        """验证许可及账户登录"""

        self.setWindowTitle('捷安特抽管模具自动设计（当前配置文件为：{}）——版本：{}'.format(self.config_path, self.version))

        # 获取当前屏幕的宽度和高度
        screen_width = screen_size()[0]
        screen_height = screen_size()[1]
        # 设置窗口的大小和位置
        self.myWidth = int(screen_width * 0.8)
        self.myHeight = int(screen_height * 0.8)
        self.setGeometry(int(screen_width) // 2 - int(self.myWidth) // 2,
                         int(screen_height) // 2 - int(self.myHeight) // 2,
                         self.myWidth,
                         self.myHeight)

        # 创建菜单栏
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件')

        self.new_action = QAction('新建', self)
        self.new_action.triggered.connect(self.new_project)
        file_menu.addAction(self.new_action)

        self.close_action = QAction('关闭', self)
        self.close_action.triggered.connect(self.close_file)
        file_menu.addAction(self.close_action)

        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close_app)
        file_menu.addAction(exit_action)

        # 配置菜单
        config_menu = menubar.addMenu('配置')

        self.show_config_action = QAction('显示配置', self)
        self.show_config_action.triggered.connect(self.show_config)
        config_menu.addAction(self.show_config_action)

        self.load_config_action = QAction('加载配置', self)
        self.load_config_action.triggered.connect(self.load_config)
        config_menu.addAction(self.load_config_action)

        self.save_config_action = QAction('修改配置', self)
        self.save_config_action.triggered.connect(self.save_and_apply_config)
        config_menu.addAction(self.save_config_action)

        self.recover_config_action = QAction('恢复默认配置', self)
        self.recover_config_action.triggered.connect(self.init_config)
        config_menu.addAction(self.recover_config_action)

        # 账户菜单
        account_menu = menubar.addMenu('账户')

        self.show_account_action = QAction('显示账户', self)
        self.show_account_action.triggered.connect(self.show_account)
        account_menu.addAction(self.show_account_action)

        self.show_license_action = QAction('显示License', self)
        self.show_license_action.triggered.connect(self.show_license)
        account_menu.addAction(self.show_license_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助')

        self.call_help_action = QAction('联系开发者', self)
        self.call_help_action.triggered.connect(self.call_help)
        help_menu.addAction(self.call_help_action)

        # 创建工具栏
        toolbar = QToolBar('工具栏')

        # 将工具栏添加到窗口顶部
        self.addToolBar(toolbar)

        # 创建布局管理器并设置间距和边距
        toolbar_layout = toolbar.layout()

        # 设置组件之间的间距
        toolbar_layout.setSpacing(10)

        # 设置边距
        toolbar_layout.setContentsMargins(5, 5, 5, 5)

        # 抽管功能按钮
        self.btn_normal = QPushButton('普通抽')
        self.btn_normal.setToolTip('普通抽')
        self.btn_normal.clicked.connect(self.Normal)
        toolbar.addWidget(self.btn_normal)

        self.btn_taper = QPushButton('TP抽')
        self.btn_taper.setToolTip('TP抽')
        self.btn_taper.clicked.connect(self.TP)
        toolbar.addWidget(self.btn_taper)

        # 数据库管理功能按钮
        toolbar1 = QToolBar('数据库管理 1')
        toolbar_layout1 = toolbar1.layout()
        toolbar_layout1.setSpacing(10)
        toolbar_layout1.setContentsMargins(5, 5, 5, 5)
        self.addToolBar(toolbar1)

        self.btn_show_all_db = QPushButton('显示所有数据')
        self.btn_show_all_db.setToolTip('显示所有数据')
        self.btn_show_all_db.clicked.connect(self.show_all_data)
        toolbar1.addWidget(self.btn_show_all_db)

        self.btn_show_all_mold_db = QPushButton('显示模具数据')
        self.btn_show_all_mold_db.setToolTip('显示模具数据')
        self.btn_show_all_mold_db.clicked.connect(self.show_all_mold_data)
        toolbar1.addWidget(self.btn_show_all_mold_db)

        toolbar2 = QToolBar('数据库管理 2')
        toolbar_layout2 = toolbar2.layout()
        toolbar_layout2.setSpacing(10)
        toolbar_layout2.setContentsMargins(5, 5, 5, 5)
        self.addToolBar(toolbar2)

        # 文本框长度
        text_box_length = 120

        self.bicycle_searchBox = QLineEdit()
        self.bicycle_searchBox.setPlaceholderText('搜索车种规格')
        self.bicycle_searchBox.setFixedWidth(text_box_length)
        toolbar2.addWidget(self.bicycle_searchBox)

        self.btn_search_key = QPushButton('搜索-车种规格')
        self.btn_search_key.setToolTip('搜索-车种规格')
        self.btn_search_key.clicked.connect(self.search_by_Bicycle_Frame_Information)
        toolbar2.addWidget(self.btn_search_key)

        self.parameter_delate_Box = QLineEdit()
        self.parameter_delate_Box.setPlaceholderText('删除车种规格')
        self.parameter_delate_Box.setFixedWidth(text_box_length)
        toolbar2.addWidget(self.parameter_delate_Box)

        self.btn_delete = QPushButton('删除-车种规格')
        self.btn_delete.setToolTip('删除-车种规格')
        self.btn_delete.clicked.connect(self.delete_by_Bicycle_Frame_Information)
        toolbar2.addWidget(self.btn_delete)

        toolbar3 = QToolBar('数据库管理 3')
        toolbar_layout3 = toolbar3.layout()
        toolbar_layout3.setSpacing(10)
        toolbar_layout3.setContentsMargins(5, 5, 5, 5)
        self.addToolBar(toolbar3)

        self.parameter_searchBox = QLineEdit()
        self.parameter_searchBox.setPlaceholderText('搜索图号')
        self.parameter_searchBox.setFixedWidth(text_box_length)
        toolbar3.addWidget(self.parameter_searchBox)

        self.btn_search_value = QPushButton('搜索-图号')
        self.btn_search_value.setToolTip('搜索-图号')
        self.btn_search_value.clicked.connect(self.search_by_graph_number)
        toolbar3.addWidget(self.btn_search_value)

        self.value_delate_Box = QLineEdit()
        self.value_delate_Box.setPlaceholderText('删除图号')
        self.value_delate_Box.setFixedWidth(text_box_length)
        toolbar3.addWidget(self.value_delate_Box)

        self.btn_delete_value = QPushButton('删除-图号')
        self.btn_delete_value.setToolTip('删除-图号')
        self.btn_delete_value.clicked.connect(self.delete_by_graph_number)
        toolbar3.addWidget(self.btn_delete_value)

        # 创建中央核心窗口
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建中央部件的垂直布局
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(5, 5, 5, 5)

        # 创建一个整体控件
        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(0)
        self.frame.setFixedHeight(int(self.myHeight * 0.7))

        # 设置整体控件的布局和策略
        self.frame_layout = QVBoxLayout()

        # 初始界面信息
        init_textedit = QTextEdit(self.frame)

        init_textedit.setText(self.init_html_text)

        self.frame_layout.addWidget(init_textedit)

        self.frame.setLayout(self.frame_layout)
        self.frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # 添加整体控件到中央布局
        self.central_layout.addWidget(self.frame)

        # frame_widget_list：用于存储frame_layout中的控件，方便后续删除（极其重要）
        self.frame_widget_list = []
        self.frame_widget_list.append(init_textedit)

        # 底部日志输出部分

        # 创建底部文本框
        self.bottomTextBox = QTextEdit()

        # 设置为只读
        self.bottomTextBox.setReadOnly(True)
        self.bottomTextBox.setText("这里将输出日志里的内容。")

        # 创建底部布局，并添加底部文本框
        bottomLayout = QVBoxLayout()
        bottomWidget = QWidget()
        bottomWidget.setLayout(bottomLayout)

        # 在底部文本框上方添加“日志输出”标签
        logLabel = QLabel("日志输出：")
        logLabel.setAlignment(Qt.AlignLeft)

        # 将标签和文本框添加到底部布局中
        bottomLayout.addWidget(logLabel)
        bottomLayout.addWidget(self.bottomTextBox)

        # 让文本框填充水平空间
        bottomLayout.setStretchFactor(self.bottomTextBox, 1)

        # 移除底部布局的边距
        bottomLayout.setContentsMargins(0, 0, 0, 0)

        # 将底部布局添加到中央部件的垂直布局中
        self.central_layout.addWidget(bottomWidget)

        self.logger.info("项目初始化成功！")

        # 更新日志
        self.update_log()

    def Normal(self):
        """普通抽界面初始化功能

        适用于DC0121、DC0124、DC0125等机器类型。
        """

        # 是否需要增加额外壁厚
        self.Normal_Add = False

        # 初始化自行车框架信息，该信息来自导入的文件名称
        self.Bicycle_Frame_Information = ''

        # 删除原有的控件
        for w in self.frame_widget_list:
            self.frame_layout.removeWidget(w)
            w.deleteLater()
        self.frame_widget_list.clear()

        # 创建普通抽工具栏
        toolbar = QToolBar('普通抽工具栏')

        # 创建布局管理器并设置间距和边距
        layout = toolbar.layout()
        # 设置组件之间的间距
        layout.setSpacing(10)
        # 设置边距
        layout.setContentsMargins(5, 5, 5, 5)

        # 增加功能按钮
        self.btn_normal_import = QPushButton('导入管件的DXF文件')
        self.btn_normal_import.setToolTip('导入管件的DXF文件')
        self.btn_normal_import.clicked.connect(self.normal_import_file)
        toolbar.addWidget(self.btn_normal_import)

        # 选择机器类型
        self.machine_type_label = QLabel("选择机器类型：", self)
        self.machine_type_comboBox = QComboBox(self)

        try:
            self.machine_type_comboBox.activated[str].connect(self._normal_add_changed_) # 点击下拉框触发事件
        except Exception as e:
            temp_str = "AppUIDemo -> Normal -> self.machine_type_comboBox.activated[str].connect(self.normal_add_changed) 报错信息：{}".format(e)
            QMessageBox.information(self, "普通抽", temp_str)
            print(temp_str)
            self.logger.error('机器类型下拉框报错：\n'+temp_str)
            return None

        self.machine_type_comboBox.addItem("DC0124") # 默认选择DC0124
        self.machine_type_comboBox.addItem("DC0121")
        self.machine_type_comboBox.addItem("DC0125")

        toolbar.addWidget(self.machine_type_label)
        toolbar.addWidget(self.machine_type_comboBox)

        # 选择额外壁厚
        self.Add_label = QLabel("是否需要增加额外壁厚：", self)
        self.Normal_Add_comboBox = QComboBox(self)

        try:
            self.Normal_Add_comboBox.activated[str].connect(self._normal_add_changed_)  # 点击下拉框触发事件
        except Exception as e:
            temp_str = "AppUIDemo -> Normal -> Normal_Add_comboBox.activated[str].connect(self.normal_add_changed) 报错信息：{}".format(e)
            QMessageBox.information(self, "普通抽", temp_str)
            print(temp_str)
            self.logger.error('增加额外壁厚下拉框报错：\n'+temp_str)
            return None

        # 向下拉框添加选项
        self.Normal_Add_comboBox.addItem("否")
        self.Normal_Add_comboBox.addItem("是")

        # 将标签和下拉框添加到工具栏
        toolbar.addWidget(self.Add_label)
        toolbar.addWidget(self.Normal_Add_comboBox)

        # 选择需要加工的模具，首先默认这几个，之后会根据机器类型和是否增加额外壁厚进行调整
        mold_name = ['裁剪夹模', '缩管模', '抽管芯轴', '抽管退料模']

        # 创建ComboCheckBox并添加到布局中
        self.comboCheckBox = ComboCheckBox(mold_name)
        self.comboCheckBox.setFixedWidth(300)
        toolbar.addWidget(self.comboCheckBox)

        self.btn_normal_caculate = QPushButton('计算模具参数')
        self.btn_normal_caculate.setToolTip('计算模具参数')
        self.btn_normal_caculate.clicked.connect(self.normal_calculate)
        toolbar.addWidget(self.btn_normal_caculate)

        self.btn_normal_save = QPushButton('保存模具参数')
        self.btn_normal_save.setToolTip('保存模具参数')
        self.btn_normal_save.clicked.connect(self.save_params_to_db)
        toolbar.addWidget(self.btn_normal_save)

        self.btn_normal_export = QPushButton('导出模具的DXF文件')
        self.btn_normal_export.setToolTip('导出模具的DXF文件')
        self.btn_normal_export.clicked.connect(self.normal_export_file)
        toolbar.addWidget(self.btn_normal_export)

        # 将工具栏添加到窗口顶部
        self.frame_layout.addWidget(toolbar)
        self.frame_widget_list.append(toolbar)

        '''如果没有导入文件，不允许点击的按钮设置为不可点击'''
        self.btn_normal_import.setDisabled(False)
        self.machine_type_comboBox.setDisabled(True)
        self.Normal_Add_comboBox.setDisabled(True)
        self.btn_normal_caculate.setDisabled(True)
        self.btn_normal_save.setDisabled(True)
        self.btn_normal_export.setDisabled(True)

        # 创建一个Tab控件，用于显示不同的功能
        self.normal_tabs = QTabWidget()
        self.normal_tabs_layout = QHBoxLayout()

        # 创建一个列表，用于存储Tab控件中的控件，方便后续删除
        self.normal_tabs_widget_list = []

        # 创建一个QLabel实例，用于显示普通抽界面的HTML文本
        norm_text = QTextEdit(self.normal_tabs)

        norm_text.setText(self.normal_html_text)

        # 将label添加到布局中
        self.normal_tabs_layout.addWidget(norm_text)

        # 将label添加到Tab控件中
        self.normal_tabs.addTab(norm_text, "须知")

        # 将label添加到列表中
        self.normal_tabs_widget_list.append(norm_text)

        # 将工具栏添加到窗口顶部
        self.frame_layout.addWidget(self.normal_tabs)

        # 将Tab控件添加到整体控件中
        self.frame_widget_list.append(self.normal_tabs)

        self.logger.info("普通抽功能初始化成功！")
        self.update_log()

    def normal_import_file(self):
        """导入制作好的普通抽管文件"""

        # 通过文件管理器选择导入文件
        file_path_tuple = QFileDialog.getOpenFileName(self, "选择文件", "./", "DXF Files (*.dxf)")
        if file_path_tuple[0] == '':
            QMessageBox.information(self, "导入文件", "未选择文件！")
            self.logger.info("未选择文件！")
            self.update_log()
            return None

        # 实例化抽管类
        try:
            self.shrink_tube_instance = ShrinkTubeClass(self.logger, file_path_tuple[0])
            # 获取文件名，保存自行车框架信息
            self.Bicycle_Frame_Information = self.shrink_tube_instance.external_params['车种规格']
            # 获取管件参数
            tube_params = self.shrink_tube_instance.get_tube_params()
            # tube_params : dict; 管件参数
        except Exception as e:
            temp_str = "AppUIDemo -> normal_import_file -> self.shrink_tube_instance = ShrinkTubeClass(self.logger, file_path_tuple[0]) 报错信息：{}".format(e)
            QMessageBox.information(self, "导入文件", temp_str)
            self.logger.error(temp_str)
            print(temp_str)
            self.update_log()
            return None

        # 导入管件的参数描述
        with open('bin/model/Normal/Parameter_Description.json', 'r', encoding='utf-8') as file:
            Parameter_Description = json.load(file)

        # 删除原有的控件
        for w in self.normal_tabs_widget_list:
            self.normal_tabs_layout.removeWidget(w)
            w.deleteLater()
        self.normal_tabs_widget_list.clear()

        # 创建表格控件
        keys = list(tube_params.keys())

        tableWidget = QTableWidget()
        tableWidget.setRowCount(len(keys))
        tableWidget.setColumnCount(3)
        tableWidget.setColumnWidth(1, 300)
        tableWidget.setColumnWidth(2, 300)
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        headers = ["参数", "值", "描述"]
        tableWidget.setHorizontalHeaderLabels(headers)

        for i in range(len(keys)):
            item = QTableWidgetItem(keys[i])
            item.setTextAlignment(Qt.AlignCenter)
            tableWidget.setItem(i, 0, item)

            item = QTableWidgetItem(str(tube_params[keys[i]]))
            item.setTextAlignment(Qt.AlignCenter)
            tableWidget.setItem(i, 1, item)

            item = QTableWidgetItem(Parameter_Description['管件参数'][keys[i]])
            item.setTextAlignment(Qt.AlignCenter)
            tableWidget.setItem(i, 2, item)

        self.normal_tabs_layout.addWidget(tableWidget)
        self.normal_tabs_widget_list.append(tableWidget)

        self.normal_tabs.addTab(tableWidget, self.Bicycle_Frame_Information)

        self.Normal_Add_comboBox.setDisabled(False)
        self.btn_normal_import.setDisabled(False)
        self.machine_type_comboBox.setDisabled(False)
        self.comboCheckBox.setDisabled(False)
        self.btn_normal_caculate.setDisabled(False)
        self.btn_normal_save.setDisabled(True)
        self.btn_normal_export.setDisabled(True)

        self.logger.info("导入文件成功！")
        self.update_log()

    def _normal_add_changed_(self):
        """增加额外壁厚下拉框触发事件

        选择是否增加额外壁厚，会影响计算的模具。
        """
        DC0124_No_Forming = ['裁剪夹模', '缩管模', '抽管芯轴', '抽管退料模']
        DC0124_Forming = ['裁剪夹模', '成型模', '成型芯轴', '成型退料模', '缩管模', '抽管芯轴', '抽管退料模']

        DC0121_No_Forming = ['裁剪夹模1', '裁剪夹模2', '缩管模', '抽管芯轴', '抽管退料模']
        DC0121_Forming = ['裁剪夹模1', '裁剪夹模2', '成型模', '成型芯轴', '成型退料模', '缩管模', '抽管芯轴', '抽管退料模']

        DC0125_No_Forming = ['裁剪夹模', '缩管模', '抽管芯轴', '抽管退料模']
        DC0125_Forming = ['裁剪夹模', '成型模', '成型芯轴', '成型退料模', '缩管模', '抽管芯轴', '抽管退料模']

        # TODO：不同的机器的模具是不同的，需要修改

        if self.Normal_Add_comboBox.currentText() == "是":
            self.Normal_Add = True
        else:
            self.Normal_Add = False

        if self.Normal_Add:
            # 额外壁厚，增加成型模具
            if self.machine_type_comboBox.currentText() == "DC0124":
                self.comboCheckBox.clearItems()
                self.comboCheckBox.addItems(DC0124_Forming)
            elif self.machine_type_comboBox.currentText() == "DC0121":
                self.comboCheckBox.clearItems()
                self.comboCheckBox.addItems(DC0121_Forming)
            elif self.machine_type_comboBox.currentText() == "DC0125":
                self.comboCheckBox.clearItems()
                self.comboCheckBox.addItems(DC0125_Forming)
        else:
            # 不增加额外壁厚，取消成型模具
            if self.machine_type_comboBox.currentText() == "DC0124":
                self.comboCheckBox.clearItems()
                self.comboCheckBox.addItems(DC0124_No_Forming)
            elif self.machine_type_comboBox.currentText() == "DC0121":
                self.comboCheckBox.clearItems()
                self.comboCheckBox.addItems(DC0121_No_Forming)
            elif self.machine_type_comboBox.currentText() == "DC0125":
                self.comboCheckBox.clearItems()
                self.comboCheckBox.addItems(DC0125_No_Forming)

    def normal_calculate(self):
        """普通抽计算模具参数"""

        # 选择机器类型
        machine_type = self.machine_type_comboBox.currentText()

        # 选择计算的模具
        mold_list = self.comboCheckBox.getSelectedItems()

        if len(mold_list) == 0:
            # 未选择计算的模具
            QMessageBox.information(self, "计算模具参数", "未选择计算的模具！")
            self.logger.error("未选择计算的模具！")
            self.update_log()
            return None

        try:
            self.shrink_tube_instance.calculate(self.user_name, self.config_setting_instance, self.Normal_Add, mold_list, machine_type)
        except Exception as e:
            temp_str = "AppUIDemo -> normal_calculate -> self.shrink_tube_instance.caculate(self.user_name, self.config_setting_instance, self.Normal_Add, mold_list, machine_type) 报错信息：{}".format(e)
            QMessageBox.information(self, "计算模具参数",temp_str)
            self.logger.error("计算模具参数失败！,错误位置：\n"+temp_str)
            print(temp_str)
            self.update_log()
            return None

        caculate_results = self.shrink_tube_instance.get_all_params()
        # caculate_results : dict; 计算结果

        # print('计算结果如下：')
        # pprint(caculate_results)

        # 导入模具的参数描述和计算方法
        with open('bin/model/Normal/Parameter_Description.json', 'r', encoding='utf-8') as file:
            Parameter_Description = json.load(file)
        with open('bin/model/Normal/Parameter_Calculate_Method.json', 'r', encoding='utf-8') as file:
            Parameter_Calculate_Method = json.load(file)

        # 删除原有的控件
        for w in self.normal_tabs_widget_list:
            self.normal_tabs_layout.removeWidget(w)
            w.deleteLater()
        self.normal_tabs_widget_list.clear()

        # 创建表格控件
        first_tabs = QTabWidget()
        first_tabs_layout = QVBoxLayout()

        self.TableWidget_dict = {}

        for key1 in caculate_results.keys():
            second_tabs = QTabWidget()
            second_tabs_layout = QVBoxLayout()

            dict1 = caculate_results[key1]

            tableWidget = QTableWidget()
            tableWidget.setRowCount(len(dict1))
            tableWidget.setColumnCount(4)
            tableWidget.setColumnWidth(1, 300)
            tableWidget.setColumnWidth(2, 300)
            tableWidget.setColumnWidth(3, 800)
            # tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

            headers = ["参数", "值", "描述", "计算方法"]
            tableWidget.setHorizontalHeaderLabels(headers)

            keys = list(dict1.keys())

            for i in range(len(keys)):
                item = QTableWidgetItem(keys[i])
                item.setTextAlignment(Qt.AlignCenter)
                tableWidget.setItem(i, 0, item)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                item = QTableWidgetItem(str(dict1[keys[i]]))
                item.setTextAlignment(Qt.AlignCenter)
                tableWidget.setItem(i, 1, item)
                if key1 == '管件参数':
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                else:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)

                # INFO: 使用图表进行显示，均会遇到这个问题

                if len(key1) > 6:  # 使用图号的关键字作为key1
                    temp = key1[:-4] # 使用大图号加小图号，不包括编号
                else:
                    temp = key1

                # print(key1, keys[i]) # key1是模具图号，keys[i]是参数名

                item = QTableWidgetItem(Parameter_Description[temp][keys[i]])
                item.setTextAlignment(Qt.AlignCenter)
                tableWidget.setItem(i, 2, item)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                item = QTableWidgetItem(Parameter_Calculate_Method[temp][keys[i]])
                item.setTextAlignment(Qt.AlignCenter)
                tableWidget.setItem(i, 3, item)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            self.TableWidget_dict[key1] = tableWidget

            second_tabs_layout.addWidget(tableWidget)
            second_tabs.setLayout(second_tabs_layout)

            first_tabs_layout.addWidget(second_tabs)
            first_tabs.addTab(second_tabs, key1)

        self.normal_tabs_layout.addWidget(first_tabs)
        self.normal_tabs_widget_list.append(first_tabs)

        self.normal_tabs.addTab(first_tabs, self.Bicycle_Frame_Information)

        self.btn_normal_import.setDisabled(True)
        self.machine_type_comboBox.setDisabled(True)
        self.Normal_Add_comboBox.setDisabled(True)
        self.comboCheckBox.setDisabled(True)
        self.btn_normal_caculate.setDisabled(True)
        self.btn_normal_save.setDisabled(False)
        self.btn_normal_export.setDisabled(True)

        QMessageBox.information(self, "计算模具参数", "计算成功！")

        self.logger.info("计算模具参数成功！")

        self.update_log()

        print('计算模具参数成功！')

    def _change_params_from_tab_(self):
        """从表格导出模具参数，同时修改不同模具的参数"""

        for graph_number in self.TableWidget_dict.keys():
            tableWidget = self.TableWidget_dict[graph_number]

            rows = tableWidget.rowCount()

            mold_name = ''
            for i in range(rows):  # 获取模具名称
                key = tableWidget.item(i, 0).text()
                value = tableWidget.item(i, 1).text()
                if key == '模具名称':
                    # 将模具名称赋值给mold_name，因为原始的mold_name是图号
                    mold_name = value
                    break

            for i in range(rows):  # 逐个元素修改参数
                key = tableWidget.item(i, 0).text()
                value = tableWidget.item(i, 1).text()
                if graph_number == '管件参数':
                    pass
                else:
                    # 通过抽管实例修改参数
                    self.shrink_tube_instance.modify_parameters(mold_name, key, value)

        self.logger.info("从表格导出模具参数成功！")

    def save_params_to_db(self):
        """保存模具参数到数据库

        如果已经有过该车架信息的参数，则进行覆盖处理。
        新车架直接保存。
        """

        # 获取计算之后的所有参数，逐一对比是否有修改
        caculate_results = self.shrink_tube_instance.get_all_params()

        Table_changed = False
        for key1 in self.TableWidget_dict.keys():
            tableWidget = self.TableWidget_dict[key1]
            rows = tableWidget.rowCount()
            for i in range(rows):
                key = tableWidget.item(i, 0).text()
                value = tableWidget.item(i, 1).text()
                if key in caculate_results[key1].keys():
                    if str(caculate_results[key1][key]) != value:
                        Table_changed = True
                        self.logger.info("表格中数据已经被修改！具体位置修改为：{}-{}-{}".format(key1, key, value))
                        self.logger.info("原始数据为：{}；修改后的数据为{}".format(caculate_results[key1][key], value))
                        self.update_log()
                        break
            if Table_changed:
                # 只要知道表格修改过，即可跳出循环
                break

        # 如果表格修改过，则询问是否保存修改之后的表格
        if Table_changed:
            reply = QMessageBox.question(self, '警告', '表格中数据已经被修改，是否保存修改后的数据？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                QMessageBox.information(self, "保存模具参数", "未保存修改后的模具参数！")
                self.logger.info("未保存修改后的模具参数！")
                self.update_log()
                return None
            elif reply == QMessageBox.Yes:
                self._change_params_from_tab_()

        # mold_name = []  # 计算后的模具参数
        # for key1 in caculate_results.keys():
        #     if key1 != '管件参数':
        #         mold_name.append(key1)

        # 查询数据库中是否已经存在这个车种规格的数据
        try:
            # 搜索这个车种规格的数据是否存在
            data = self.crypto_data_instance.query_data_by_Bicycle_Frame_Information(self.Bicycle_Frame_Information)
        except Exception as e:
            temp_str = "AppUIDemo -> save_params_to_db -> self.crypto_data_instance.query_data_by_Bicycle_Frame_Information(self.Bicycle_Frame_Information) 报错信息：{}".format(e)
            QMessageBox.information(self, "保存模具参数", temp_str)
            print(temp_str)
            self.logger.error("查询数据失败！报错位置:\n"+temp_str)
            self.update_log()
            data = {}

        # 已经存在这个车种规格的数据
        if data != {}:
            reply = QMessageBox.question(self, '警告',
                                         '已存在{}的模具数据，是否覆盖？'.format(self.Bicycle_Frame_Information),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # 覆盖保存，原来的数据将被删除，新的数据将被保存
                self.crypto_data_instance.delete_Bicycle_Frame_Information(self.Bicycle_Frame_Information)

                self.shrink_tube_instance.save_all()

                # inside_mold = []
                # outside_mold = []
                # for key in data:
                #     next_dict = data[key]
                #     for mold in mold_name:
                #         if mold in next_dict.keys():
                #             inside_mold.append(mold) # 需要覆盖的模具
                #
                # for name in mold_name:
                #     if name not in inside_mold:
                #         outside_mold.append(name)
                #
                # # print(inside_mold, outside_mold)
                # # 保存新增的模具
                # for mold in outside_mold:
                #     '''按照车种规格和模具名保存数据'''
                #     for key in data:
                #         self.crypto_data_instance.save_by_key_and_graph_number(key, mold, caculate_results[mold])
                #         self.logger.info("成功保存{}模具参数！".format(mold))
                #         self.update_log()
                # if outside_mold != []:
                #     QMessageBox.information(self, "保存模具参数", "新增模具参数保存成功！")
                #
                # # 覆盖已有的模具
                # for mold in inside_mold: # 对每个模具都作处理
                #     for key in data:
                #         next_dict = data[key]
                #         graph_number = next_dict[mold]['图号']
                #         reply = QMessageBox.question(self, '警告', '已存在{}的模具数据，原始图号为{}，是否覆盖？'.format(mold, graph_number),
                #                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                #         if reply == QMessageBox.Yes:
                #             # 删除原来的图号
                #             self.crypto_data_instance.delete_graph_number(graph_number)
                #             # 保存新的数据
                #             self.crypto_data_instance.save_by_key_and_graph_number(key, mold, caculate_results[mold])
                #             self.logger.info("成功覆盖保存{}模具参数！".format(mold))
                #             self.update_log()
                #         elif reply == QMessageBox.No:
                #             self.logger.info("未保存{}模具参数！".format(mold))
                #             self.update_log()

                # if inside_mold != []:
                #     QMessageBox.information(self, "保存模具参数", "覆盖保存成功！")

                QMessageBox.information(self, "保存模具参数", "覆盖保存模具参数成功！")
                self.logger.info("覆盖保存模具参数成功！")
                self.update_log()
            else:
                QMessageBox.information(self, "保存模具参数", "未保存模具参数！")
                self.logger.info("未保存模具参数！")
                self.update_log()
                return None
        else:
            # 直接保存
            self.shrink_tube_instance.save_all()

            QMessageBox.information(self, "保存模具参数", "成功保存模具参数！")
            self.logger.info("保存模具参数成功！")
            self.update_log()

        self.btn_normal_import.setDisabled(True)
        self.Normal_Add_comboBox.setDisabled(True)
        self.comboCheckBox.setDisabled(True)
        self.btn_normal_caculate.setDisabled(True)
        self.btn_normal_save.setDisabled(False)
        self.btn_normal_export.setDisabled(False)

        # print('def save_params_to_db: end')

    def normal_export_file(self):
        """导出普通抽的DXF和Excel文件

        导出的文件位置可以自己选择，也可以使用默认位置。
        """

        try:
            reply = QMessageBox.question(self, '提醒', '自定义导出文件夹？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                save_path = QFileDialog.getExistingDirectory(self, "选择保存路径", "./")
                if save_path == '':
                    QMessageBox.information(self, "导出文件", "未选择保存路径！")
                    self.logger.info("未选择保存路径！")
                    self.update_log()
                    return None
                else:
                    save_path = save_path + '/' + self.Bicycle_Frame_Information
                    # if os.path.exists(save_path):
                    os.makedirs(save_path)
                    self.logger.info("自定义路径保存参数成功！路径为：" + save_path)
                    '''判断是否是空文件夹'''
                    if os.listdir(save_path):
                        reply1 = QMessageBox.question(self, '警告', '该文件夹存在数据，是否覆盖？',
                                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if reply1 == QMessageBox.Yes:
                            self.shrink_tube_instance.output_dxf(save_path)
                            self.shrink_tube_instance.output_excel(save_path)

                            QMessageBox.information(self, "导出文件", "覆盖保存成功！路径为：" + save_path)
                            self.logger.info("覆盖保存成功！路径为：" + save_path)
                        else:
                            QMessageBox.information(self, "导出文件", "未保存文件！")
                            self.logger.info("未保存文件！")
                            self.update_log()
                            return None
                    else:
                        self.shrink_tube_instance.output_dxf(save_path)
                        self.shrink_tube_instance.output_excel(save_path)

                        QMessageBox.information(self, "保存模具参数", "自定义路径保存参数成功！路径为：" + save_path)
                        self.logger.info("自定义路径保存参数成功！路径为：" + save_path)
            elif reply == QMessageBox.No:
                '''如果没有选择自定义路径,则使用默认路径'''
                reply1 = QMessageBox.question(self, '提醒', '是否使用默认路径？', QMessageBox.Yes | QMessageBox.No,
                                              QMessageBox.No)
                if reply1 == QMessageBox.Yes:
                    save_path = os.path.join(os.getcwd(), 'output/' + self.Bicycle_Frame_Information)
                    save_path_new = save_path

                    index = 1
                    while os.path.exists(save_path_new):
                        save_path_new = save_path + '_' + str(index)
                        index += 1

                    os.makedirs(save_path_new)

                    self.shrink_tube_instance.output_dxf(save_path_new)
                    self.shrink_tube_instance.output_excel(save_path_new)

                    QMessageBox.information(self, "保存模具参数", "使用默认路径保存参数成功！路径为：" + save_path_new)
                    self.logger.info("使用默认路径保存参数成功！路径为：" + save_path_new)
                elif reply1 == QMessageBox.No:
                    QMessageBox.information(self, "导出文件", "未保存文件！")
                    self.logger.info("未保存文件！")
            self.update_log()
        except Exception as e:
            temp_str = "AppUIDemo -> normal_export_file -> self.shrink_tube_instance.output_dxf(save_path) 报错信息：{}".format(e)
            QMessageBox.information(self, "导出文件", temp_str)
            self.logger.error("导出文件失败！报错位置：\n"+temp_str)
            self.update_log()
            return None

    def TP(self):
        """TP抽功能

        还未实现。
        """

        # 自行车车架信息
        self.Bicycle_Frame_Information = ''

        # 删除原有的控件
        # for w in self.frame_widget_list:
        #     self.frame_layout.removeWidget(w)
        #     w.deleteLater()
        # self.frame_widget_list.clear()

        QMessageBox.information(self, "Type抽", "Type抽功能还未完善，敬请期待！")
        self.logger.info("Type抽功能还未完善，敬请期待！")
        self.update_log()

    def show_all_data(self):
        """数据库操作：显示所有项目数据"""

        try:
            data = self.crypto_data_instance.decrypt_all_project()
        except Exception as e:
            temp_str = "AppUIDemo -> show_all_data -> self.crypto_data_instance.decrypt_all_project() 报错信息：{}".format(e)
            QMessageBox.information(self, "显示所有项目数据", "显示所有项目数据失败！报错位置：\n"+temp_str)
            self.logger.error("显示所有项目数据失败！报错位置：\n"+temp_str)
            self.update_log()
            return None

        try:
            resultDialog = ReserachResultDialog(self)
            resultDialog.initUI(data)
            resultDialog.exec_()
            self.logger.info("显示所有项目数据成功！")
            self.update_log()
        except Exception as e:
            temp_str = "AppUIDemo -> show_all_data -> resultDialog.initUI(data) 报错信息：{}".format(e)
            QMessageBox.information(self, "显示所有项目数据", "显示所有项目数据失败！报错位置：\n"+temp_str)
            self.logger.error("显示所有项目数据失败！报错位置：\n"+temp_str)
            self.update_log()
            return None

    def show_all_mold_data(self):
        """数据库操作：显示所有模具数据"""

        try:
            resultDialog = ReserachResultDialog_Mold(self)
            resultDialog.initUI(self.crypto_data_instance)
            resultDialog.exec_()
            self.logger.info("显示所有模具数据成功！")
            self.update_log()
        except Exception as e:
            temp_str = "AppUIDemo -> show_all_mold_data -> resultDialog.initUI(data) 报错信息：{}".format(e)
            QMessageBox.information(self, "显示所有模具数据", "显示所有数据失败！报错位置：\n"+temp_str)
            self.logger.error("显示所有模具数据失败！报错位置：\n"+temp_str)
            self.update_log()
            return None

    def search_by_Bicycle_Frame_Information(self):
        """数据库操作：根据车架号搜索项目数据"""

        search_text = self.bicycle_searchBox.text()

        if search_text == "":
            QMessageBox.information(self, "搜索", "搜索框为空，请输入搜索内容！")
            self.logger.info("搜索框为空，请输入搜索内容！")
            self.update_log()
            return None

        try:
            data = self.crypto_data_instance.query_data_by_Bicycle_Frame_Information(search_text)
        except Exception as e:
            temp_str = "AppUIDemo -> search_by_Bicycle_Frame_Information -> self.crypto_data_instance.query_data_by_Bicycle_Frame_Information(search_text) 报错信息：{}".format(e)
            QMessageBox.information(self, "搜索", "未找到搜索内容！报错位置：\n"+temp_str)
            self.logger.error("未找到搜索内容！报错位置：\n"+temp_str)
            self.update_log()
            return

        if data == None or data == {}:
            QMessageBox.information(self, "搜索", "未找到搜索内容！")
            self.logger.info(f"未找到搜索内容：{search_text}")
            self.update_log()
            return None

        try:
            resultDialog = ReserachResultDialog(self)
            resultDialog.initUI(data)
            resultDialog.exec_()

            self.logger.info(f"搜索{search_text}成功！")
            self.update_log()
        except Exception as e:
            temp_str = "AppUIDemo -> search_by_Bicycle_Frame_Information -> resultDialog.initUI(data) 报错信息：{}".format(e)
            QMessageBox.information(self, "搜索", "搜索车架号失败！报错位置：\n"+temp_str)
            self.logger.error("搜索车架号失败！报错位置：\n"+temp_str)
            self.update_log()
            return None

    def search_by_graph_number(self):
        """数据库操作：根据图号搜索项目数据"""

        search_text = self.parameter_searchBox.text()

        if search_text == "":
            QMessageBox.information(self, "搜索", "搜索框为空，请输入搜索内容！")
            self.logger.info("搜索框为空，请输入搜索内容！")
            self.update_log()
            return None

        try:
            data = self.crypto_data_instance.query_data_by_graph_number(search_text)
            select = {}
            for key in data.keys():
                select[key] = {}
                rest_dict = data[key]
                for key1 in rest_dict.keys():
                    if key1 != '管件参数' and rest_dict[key1]['图号'] == search_text:
                        select[key][key1] = rest_dict[key1]
                        break
            data = select
        except Exception as e:
            temp_str = "AppUIDemo -> search_by_graph_number -> self.crypto_data_instance.query_data_by_graph_number(search_text) 报错信息：{}".format(e)
            QMessageBox.information(self, "搜索", "未找到搜索内容！报错位置：\n"+temp_str)
            self.logger.error("未找到搜索内容！报错位置：\n"+temp_str)
            self.update_log()
            return

        if data == None or data == {}:
            QMessageBox.information(self, "搜索", "未找到搜索内容！")
            self.logger.info(f"未找到搜索内容：{search_text}")
            self.update_log()
            return None

        try:
            resultDialog = ReserachResultDialog(self)
            resultDialog.initUI(data)
            resultDialog.exec_()

            self.logger.info(f"搜索{search_text}成功！")
            self.update_log()
        except Exception as e:
            temp_str = "AppUIDemo -> search_by_graph_number -> resultDialog.initUI(data) 报错信息：{}".format(e)
            QMessageBox.information(self, "搜索", "搜索图号失败！报错位置：\n"+temp_str)
            self.logger.error("搜索图号失败！报错位置：\n"+temp_str)
            self.update_log()
            return None

    def delete_by_Bicycle_Frame_Information(self):
        """数据库操作：根据车架号删除项目数据"""

        search_text = self.parameter_delate_Box.text()

        if search_text == "":
            QMessageBox.information(self, "搜索", "搜索框为空，请输入搜索内容！")
            self.logger.info("搜索框为空，请输入搜索内容！")
            self.update_log()
            return None

        try:
            data = self.crypto_data_instance.query_data_by_Bicycle_Frame_Information(search_text)
        except Exception as e:
            temp_str = "AppUIDemo -> delete_by_Bicycle_Frame_Information -> self.crypto_data_instance.query_data_by_Bicycle_Frame_Information(search_text) 报错信息：{}".format(e)
            QMessageBox.information(self, "搜索", "未找到搜索内容！报错位置：\n"+temp_str)
            self.logger.error("未找到搜索内容！报错位置：\n"+temp_str)
            self.update_log()
            return

        if data == None or data == {}:
            QMessageBox.information(self, "搜索", "未找到搜索内容！")
            self.logger.info(f"未找到搜索内容：{search_text}")
            self.update_log()
            return None

        try:
            resultDialog = ReserachResultDialog(self)
            resultDialog.initUI(data)
            resultDialog.exec_()
            self.logger.info(f"搜索{search_text}成功！")
            self.update_log()
        except Exception as e:
            temp_str = "AppUIDemo -> delete_by_Bicycle_Frame_Information -> resultDialog.initUI(data) 报错信息：{}".format(e)
            QMessageBox.information(self, "搜索", "搜索失败！报错位置：\n"+temp_str)
            self.logger.error("搜索失败！报错位置：\n"+temp_str)
            self.update_log()
            return None

        reply = QMessageBox.question(self, '警告', '是否删除该条数据？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.crypto_data_instance.delete_Bicycle_Frame_Information(search_text)
            QMessageBox.information(self, "删除", "删除成功！")
            self.logger.info(f"删除{search_text}成功！")
            self.update_log()
        elif reply == QMessageBox.No:
            QMessageBox.information(self, "删除", "未删除数据！")
            self.logger.info(f"未删除{search_text}数据！")
            self.update_log()

    def delete_by_graph_number(self):
        """数据库操作：根据图号删除项目数据"""

        search_text = self.value_delate_Box.text()

        if search_text == "":
            QMessageBox.information(self, "搜索", "搜索框为空，请输入搜索内容！")
            self.logger.info("搜索框为空，请输入搜索内容！")
            self.update_log()
            return None

        try:
            data = self.crypto_data_instance.query_data_by_graph_number(search_text)
            # pprint(data)
            select = {}
            for key in data.keys():
                select[key] = {}
                rest_dict = data[key]
                for key1 in rest_dict.keys():
                    # print(key1)
                    if key1 != '管件参数' and rest_dict[key1]['图号'] == search_text:
                        select[key][key1] = rest_dict[key1]
                        break
            # pprint(select)
            data = select
        except Exception as e:
            temp_str = "AppUIDemo -> delete_by_graph_number -> self.crypto_data_instance.query_data_by_graph_number(search_text) 报错信息：{}".format(e)
            QMessageBox.information(self, "搜索", "未找到搜索内容！报错位置：\n"+temp_str)
            self.logger.error("未找到搜索内容！报错位置：\n"+temp_str)
            self.update_log()
            return

        if data == None or data == {}:
            QMessageBox.information(self, "搜索", "未找到搜索内容！")
            self.logger.info(f"未找到搜索内容：{search_text}")
            self.update_log()
            return None

        try:
            resultDialog = ReserachResultDialog(self)
            resultDialog.initUI(data)
            resultDialog.exec_()
            self.logger.info(f"搜索{search_text}成功！")
            self.update_log()
        except Exception as e:
            temp_str = "AppUIDemo -> delete_by_graph_number -> resultDialog.initUI(data) 报错信息：{}".format(e)
            QMessageBox.information(self, "搜索", "搜索失败！报错位置：\n"+temp_str)
            self.logger.error("搜索失败！报错位置：\n"+temp_str)
            self.update_log()
            return None

        reply = QMessageBox.question(self, '警告', '是否删除该条数据？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.crypto_data_instance.delete_graph_number(search_text)
            QMessageBox.information(self, "删除", "删除成功！")
            self.logger.info(f"删除{search_text}成功！")
            self.update_log()
        elif reply == QMessageBox.No:
            QMessageBox.information(self, "删除", "未删除数据！")
            self.logger.info(f"未删除{search_text}数据！")
            self.update_log()

    def new_project(self):
        """新建项目"""

        self.Bicycle_Frame_Information = ''

        # 删除原有的控件
        for w in self.frame_widget_list:
            self.frame_layout.removeWidget(w)
            w.deleteLater()
        self.frame_widget_list.clear()

        # 创建初始界面信息
        init_textedit = QTextEdit(self.frame)

        init_textedit.setText(self.init_html_text)

        self.frame_layout.addWidget(init_textedit)
        self.frame.setLayout(self.frame_layout)
        self.frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.frame_widget_list.append(init_textedit)

        self.logger.info("新建项目成功！")
        self.update_log()

    def close_file(self):
        """关闭项目，并初始化界面"""

        self.Bicycle_Frame_Information = ''

        # 删除原有的控件
        for w in self.frame_widget_list:
            self.frame_layout.removeWidget(w)
            w.deleteLater()
        self.frame_widget_list.clear()

        # 创建初始界面信息
        init_textedit = QTextEdit(self.frame)
        # 编写HTML格式的文本，包括样式和层级
        init_textedit.setText(self.init_html_text)

        self.frame_layout.addWidget(init_textedit)
        self.frame.setLayout(self.frame_layout)
        self.frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.frame_widget_list.append(init_textedit)

        self.logger.info("关闭项目成功（未保存）！")
        self.update_log()

    def close_app(self):
        """关闭程序"""

        reply = QMessageBox.question(self, '警告', '所有未保存的都将会删除，是否退出程序？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logger.info("程序结束运行")
            self.logger.close()
            self.update_log()
            sys.exit()
        elif reply == QMessageBox.No:
            self.update_log()
            return None

    def call_help(self):
        """联系开发者"""
        QMessageBox.information(self, "联系开发者", "编辑问题邮件发送给：smaugfire@163.com。")
        self.logger.info("联系开发者")
        self.update_log()

    def update_log(self, ):
        """更新日志"""
        log_path = self.logger.get_log_path()

        with open(log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()

        self.bottomTextBox.setText(log_content)

        doc = self.bottomTextBox.document()
        cursor = QTextCursor(doc)
        start = 0

        while True:
            # 查找 "ERROR" 的位置
            start = doc.toPlainText().find("ERROR", start)
            # 如果没有找到，退出循环
            if start == -1:
                break

            end = start + len("ERROR")

            # 设置文本格式
            format = QTextCharFormat()
            format.setFontWeight(QFont.Bold)

            # 设置字体颜色为红色
            format.setForeground(QColor("red"))

            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len("ERROR"))
            cursor.setCharFormat(format)

            # 更新起始位置，继续查找下一个 "ERROR"
            start = end

        cursor = self.bottomTextBox.textCursor()
        cursor.movePosition(cursor.End)
        self.bottomTextBox.setTextCursor(cursor)

    def closeEvent(self, event):
        """关闭程序时，询问是否保存日志"""
        reply = QMessageBox.question(self, '确认退出',
                                     "未保存的数据都将删除，你确定要退出应用程序吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.logger.info("程序结束运行")
            self.logger.close()
        else:
            event.ignore()
            self.update_log()

    def show_account(self):
        """显示账户信息"""
        QMessageBox.information(self, "账户", "ID：{}\n姓名：{}".format(self.ID, self.user_name))
        self.logger.info("ID：{}\n姓名：{}".format(self.ID, self.user_name))
        self.update_log()

    def show_config(self):
        """显示配置信息"""
        config_description = self.config_setting_instance.config_description
        configresultDialog = ConfigResultDialog(self)
        configresultDialog.initUI(self.config, config_description)
        configresultDialog.exec_()
        self.logger.info("显示配置信息")
        self.update_log()

    def load_config(self):
        """加载配置文件"""

        file_path = QFileDialog.getOpenFileName(self, "选择文件", "./", "JSON Files (*.json)")

        if file_path[0] == '':
            QMessageBox.information(self, "加载配置", "未选择文件！")
            return None

        self.config_path = file_path[0]

        self.config_setting_instance = ConfigSettingClass(self.logger, file_path[0])

        # 重新加载配置文件
        self.config = self.config_setting_instance.get_all_config()

        self.setWindowTitle('捷安特抽管模具自动设计（当前配置文件为：{}）——版本：{}'.format(self.config_path, self.version))

        QMessageBox.information(self, "加载配置", "加载配置文件成功！")

        self.logger.info(f"加载配置文件成功！路径为：{file_path[0]}")
        self.update_log()

        try:
            # BUG: 为实例化的时候调用会报错，但是不影响使用
            self.btn_normal_import.setDisabled(True)
            self.btn_normal_caculate.setDisabled(True)
            self.btn_normal_save.setDisabled(True)
            self.btn_normal_export.setDisabled(True)
        except Exception as e:
            temp_str = "AppUIDemo -> load_config -> self.btn_normal_import.setDisabled(True) 报错信息：{}".format(e)
            QMessageBox.information(self, "加载配置", "加载配置文件失败！报错位置：\n"+temp_str)
            self.logger.error("加载配置文件失败！报错位置：\n"+temp_str)
            self.update_log()

    def save_and_apply_config(self):
        """保存并应用配置文件"""

        try:
            config_description = self.config_setting_instance.config_description
            modify_configresultDialog = ModifyConfigResultDialog(self)
            modify_configresultDialog.initUI(self.config, config_description)
            modify_configresultDialog.exec_()

            self.config = modify_configresultDialog.get_table_params()
            # pprint(self.config)

        except Exception as e:
            temp_str = "AppUIDemo -> save_and_apply_config -> modify_configresultDialog.initUI(self.config, config_description) 报错信息：{}".format(e)
            QMessageBox.information(self, "保存配置", "保存配置文件失败！报错位置：\n"+temp_str)
            self.logger.error("保存配置文件失败！报错位置：\n"+temp_str)
            self.update_log()
            return None

        modify_file_path = QFileDialog.getSaveFileName(self, "选择文件", "./", "JSON Files (*.json)")

        if modify_file_path[0] == '':
            QMessageBox.information(self, "保存配置", "未选择文件,保存配置文件失败, 将不会应用新的配置文件！")
            # 将所有配置数据恢复为原来的配置数据
            self.config = self.config_setting_instance.get_all_config()
            return None

        # 保存配置文件
        self.config_setting_instance.save_config(modify_file_path[0], self.config)
        QMessageBox.information(self, "保存配置", "保存配置文件成功！,路径为：{}".format(modify_file_path[0]))
        self.logger.info("保存配置文件成功！,路径为：{}".format(modify_file_path[0]))

        # 重新加载配置文件
        self.config_path = modify_file_path[0]
        self.config_setting_instance = ConfigSettingClass(self.logger, modify_file_path[0])
        self.config = self.config_setting_instance.get_all_config()

        self.setWindowTitle('捷安特抽管模具自动设计（当前配置文件为：{}）——版本：{}'.format(self.config_path, self.version))

        self.logger.info("重新加载配置文件成功！")

        try:
            self.btn_normal_import.setDisabled(True)
            self.btn_normal_caculate.setDisabled(True)
            self.btn_normal_save.setDisabled(True)
            self.btn_normal_export.setDisabled(True)
        except Exception as e:
            temp_str = "AppUIDemo -> save_and_apply_config -> self.btn_normal_import.setDisabled(True) 报错信息：{}".format(e)
            QMessageBox.information(self, "保存配置", "重新加载配置文件失败！报错位置：\n"+temp_str)
            self.logger.error("重新加载配置文件失败！报错位置：\n"+temp_str)
            return

        self.update_log()

    def init_config(self):
        """初始化配置文件"""

        self.config_setting_instance.init_config()
        self.config = self.config_setting_instance.get_all_config()
        self.config_path = 'config/default.json'

        self.setWindowTitle('捷安特抽管模具自动设计（当前配置文件为：{}）——版本：{}'.format(self.config_path, self.version))

        try:
            # BUG: 为实例化的时候调用会报错，但是不影响使用
            self.btn_normal_import.setDisabled(True)
            self.btn_normal_caculate.setDisabled(True)
            self.btn_normal_save.setDisabled(True)
            self.btn_normal_export.setDisabled(True)
        except Exception as e:
            temp_str = "AppUIDemo -> init_config -> self.btn_normal_import.setDisabled(True) 报错信息：{}".format(e)
            QMessageBox.information(self, "初始化配置文件", "初始化配置文件失败！报错位置：\n"+temp_str)
            self.logger.error("初始化配置文件失败！报错位置：\n"+temp_str)
            return

        QMessageBox.information(self, "恢复默认配置", "恢复默认配置成功！")
        self.logger.info("初始化配置文件成功！")
        self.update_log()

    def show_license(self):
        """显示License信息"""

        QMessageBox.information(self, "License", self.message)
        self.logger.info("显示License信息")
        self.update_log()


# Main program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppUiDemo()
    ex.show()
    sys.exit(app.exec_())
