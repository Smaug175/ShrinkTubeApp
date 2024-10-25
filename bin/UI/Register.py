import os

from PyQt5.QtWidgets import QMessageBox, QApplication, QVBoxLayout, QLabel, QDialog, QPushButton, QHBoxLayout, QLineEdit

os.environ['QT_SCALE_FACTOR'] = '1.1'

from bin.utils.UserInf import UserManager


def screen_size():
    """获取屏幕尺寸"""
    screen = QApplication.desktop().screenGeometry()
    return screen.width(), screen.height()


class RegisterWindow(QDialog):
    """注册窗口

    Methods
    _______
    __init__(self, parent, logger)
        初始化注册窗口
    register(self)
        注册用户
    """

    def __init__(self, parent, logger):
        """初始化注册窗口"""

        super().__init__(parent)

        self.logger = logger

        self.setWindowTitle('注册')

        screen_width = screen_size()[0]
        screen_height = screen_size()[1]
        self.myWidth = int(screen_width * 0.2)
        self.myHeight = int(screen_height * 0.2)
        self.setGeometry(int(screen_width) // 2 - int(self.myWidth) // 2,
                         int(screen_height) // 2 - int(self.myHeight) // 2,
                         self.myWidth, self.myHeight)

        # 创建垂直主布局
        main_layout = QVBoxLayout()

        # 用户名、密码和确认密码输入框
        self.ID_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        # 注册按钮
        self.register_button = QPushButton('注册')
        self.register_button.clicked.connect(self.register)

        # 为每个输入框创建水平布局
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel('ID：'))
        id_layout.addWidget(self.ID_input)

        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel('姓名：'))
        username_layout.addWidget(self.username_input)

        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel('密码：'))
        password_layout.addWidget(self.password_input)

        confirm_password_layout = QHBoxLayout()
        confirm_password_layout.addWidget(QLabel('确认密码：'))
        confirm_password_layout.addWidget(self.confirm_password_input)

        # 将水平布局添加到垂直主布局
        main_layout.addLayout(id_layout)
        main_layout.addLayout(username_layout)
        main_layout.addLayout(password_layout)
        main_layout.addLayout(confirm_password_layout)
        main_layout.addWidget(self.register_button)

        # 设置主布局
        self.setLayout(main_layout)

    def register(self):
        """注册用户"""

        # 获取用户输入的信息
        ID = self.ID_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # 简单的验证逻辑
        if not ID or not username or not password or not confirm_password:
            QMessageBox.information(self, '提示', '请填写完整信息')
            return
        if password != confirm_password:
            QMessageBox.information(self, '提示', '两次输入的密码不一致')
            return

        user_manager = UserManager(self.logger)
        information = user_manager.create_user(ID, username, password)

        if information != 'True':
            QMessageBox.information(self, '提示', information)
            return

        self.accept()  # 关闭注册窗口

        self.logger.info("用户注册成功")
        QMessageBox.information(self, '提示', '注册成功，点击确定关闭窗口')

        # 清空输入框
        self.ID_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
