import os
from PyQt5.QtWidgets import QMessageBox, QApplication, QVBoxLayout, QLabel, QDialog, QPushButton, QHBoxLayout, QLineEdit

# 设置缩放因子
os.environ['QT_SCALE_FACTOR'] = '1.1'

from bin.utils.UserInf import UserManager
from bin.UI.Register import RegisterWindow


def screen_size() -> tuple:
    """获取屏幕大小"""
    screen = QApplication.desktop().screenGeometry()
    return screen.width(), screen.height()


class LoginWindow(QDialog):
    """登录窗口

    用户登录窗口，用于用户登录和注册

    Methods
    -------
    __init__(parent, logger)
        初始化登录窗口
    login()
        登录
    get_ID_name() -> tuple
        获取用户ID和用户名
    signin()
        注册
    modify_password()
        修改密码
    """

    def __init__(self, parent, logger):
        """初始化登录窗口

        Parameters
        ----------
        parent : QWidget
            父窗口
        logger : logging.Logger
            日志记录器
        """
        super().__init__(parent)

        self.logger = logger

        self.setWindowTitle('登录')

        # 设置窗口大小和位置
        screen_width = screen_size()[0]
        screen_height = screen_size()[1]

        self.myWidth = int(screen_width * 0.2)
        self.myHeight = int(screen_height * 0.1)
        self.setGeometry(int(screen_width) // 2 - int(self.myWidth) // 2,
                         int(screen_height) // 2 - int(self.myHeight) // 2,
                         self.myWidth, self.myHeight)

        # 新建布局
        layout_all = QVBoxLayout()
        layout_ID = QHBoxLayout()
        layout_password = QHBoxLayout()

        # 用户名和密码输入框
        self.userID_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        layout_btn = QHBoxLayout()

        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self.login)

        self.signin_button = QPushButton('注册')
        self.signin_button.clicked.connect(self.signin)

        self.modify_button = QPushButton('修改密码')
        self.modify_button.clicked.connect(self.modify_password)

        # 添加控件到布局
        layout_ID.addWidget(QLabel('用户名：'))
        layout_ID.addWidget(self.userID_input)
        layout_password.addWidget(QLabel('密码：'))
        layout_password.addWidget(self.password_input)

        layout_btn.addWidget(self.login_button)
        layout_btn.addWidget(self.signin_button)
        # layout_btn.addWidget(self.modify_button)

        layout_all.addLayout(layout_ID)
        layout_all.addLayout(layout_password)
        layout_all.addLayout(layout_btn)

        # 设置布局
        self.setLayout(layout_all)

        # 初始化用户ID和用户名，一开始为空
        self.ID = None
        self.name = None

    def login(self):
        """登录

        验证用户名和密码是否正确
        """

        ID = self.userID_input.text()
        password = self.password_input.text()

        if ID == '' or password == '':
            QMessageBox.warning(self, '登录', '用户名或密码不能为空！')
            self.logger.info("用户登录失败，用户名或密码不能为空！")
            return

        try:
            user_manager = UserManager(self.logger)
            is_authenticated = user_manager.authenticate_user(ID, password)
            # is_authenticated; True: 认证成功; False: 认证失败; None: 用户名不存在
        except Exception as e:
            temp_str = ('数据库连接失败！错误位置：\n'
                        ' LoginWindow -> on_login -> user_manager.authenticate_user(ID, password) \n'
                        '错误信息：\n') + str(e)
            self.logger.error(temp_str)
            print(temp_str)
            QMessageBox.warning(self, '登录失败', '数据库连接失败！')
            self.logger.error("数据库连接失败！")
            return

        if is_authenticated is None:
            QMessageBox.warning(self, '登录失败', '用户名不存在！')
            self.logger.info("用户登录失败，用户名不存在！")
        elif is_authenticated:
            # QMessageBox.information(self, '登录成功', '登录成功！')
            self.logger.info("用户登录成功！")
            # 登录成功，保存用户ID和用户名
            self.ID = ID
            self.name = user_manager.query_user(ID)['姓名']
            self.accept()
        else:
            QMessageBox.warning(self, '登录失败', '用户名或密码错误！')
            self.logger.info("用户登录失败，用户名或密码错误！")

    def get_ID_name(self) -> tuple:
        """获取用户ID和用户名"""
        if self.ID and self.name:
            return self.ID, self.name

    def signin(self):
        """注册"""
        register_window = RegisterWindow(self, self.logger)
        if register_window.exec_():
            self.logger.info("用户注册成功,请重新登录！")
        else:
            self.logger.info("用户取消注册")

    def modify_password(self):
        """修改密码"""
        # TODO: 未实现修改用户密码
        # 这里添加修改密码逻辑
        print('修改密码')
        self.logger.info("用户修改密码")
