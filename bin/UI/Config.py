from PyQt5.QtWidgets import  QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout,  QTabWidget, QDialog,  QAbstractItemView
from PyQt5.QtCore import Qt

import os

os.environ['QT_SCALE_FACTOR'] = '1.1'


def screen_size():
    """获取屏幕尺寸"""
    screen = QApplication.desktop().screenGeometry()
    return screen.width(), screen.height()


class ConfigResultDialog(QDialog):
    """设置结果的显示界面

    该类继承自QDialog，用于显示设置结果的界面。

    Methods
    _______
    initUI(self, config: dict, config_description: dict)
        初始化界面
    """

    def __init__(self, parent=None,):
        super().__init__(parent)

    def initUI(self, config: dict, config_description: dict):
        """初始化界面"""

        self.setWindowTitle("配置结果")

        screen_width = screen_size()[0]
        screen_height = screen_size()[1]

        self.myWidth = int(screen_width * 0.5)
        self.myHeight = int(screen_height * 0.6)
        self.setGeometry(int(screen_width) // 2 - int(self.myWidth) // 2,
                         int(screen_height) // 2 - int(self.myHeight) // 2,
                         self.myWidth, self.myHeight)

        try:
            self.mainLayout = QVBoxLayout()
            self.mainLayout.setContentsMargins(5, 5, 5, 5)

            first_tabs = QTabWidget()
            first_tabs_layout = QVBoxLayout()

            for key1 in config.keys():
                second_tabs = QTabWidget()
                second_tabs_layout = QVBoxLayout()

                dict1 = config[key1]

                tableWidget = QTableWidget()
                tableWidget.setRowCount(len(dict1))
                tableWidget.setColumnCount(3)
                tableWidget.setColumnWidth(0, 300)
                tableWidget.setColumnWidth(1, 300)
                tableWidget.setColumnWidth(2, 300)
                tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

                headers = ["参数", "值", "描述"]
                tableWidget.setHorizontalHeaderLabels(headers)

                keys = list(dict1.keys())
                for i in range(len(keys)):
                    item = QTableWidgetItem(keys[i])
                    item.setTextAlignment(Qt.AlignCenter)
                    tableWidget.setItem(i, 0, item)

                    item = QTableWidgetItem(str(dict1[keys[i]]))
                    item.setTextAlignment(Qt.AlignCenter)
                    tableWidget.setItem(i, 1, item)

                    item = QTableWidgetItem(config_description[key1][keys[i]])
                    item.setTextAlignment(Qt.AlignCenter)
                    tableWidget.setItem(i, 2, item)

                second_tabs_layout.addWidget(tableWidget)
                second_tabs.setLayout(second_tabs_layout)

                first_tabs_layout.addWidget(second_tabs)
                first_tabs.addTab(second_tabs, key1)

            self.mainLayout.addWidget(first_tabs)  # 添加第一层 QTabWidget 到主布局
            self.setLayout(self.mainLayout)
        except Exception as e:
            temp_str = "配置结果界面初始化失败！报错位置：ConfigResultDialog.initUI()，错误信息：{}".format(e)
            print(temp_str)

class ModifyConfigResultDialog(QDialog):
    """修改设置结果的显示界面

    该类继承自QDialog，用于显示修改设置结果的界面。

    Methods
    _______
    initUI(self, config: dict, config_description: dict)
        初始化界面
    get_table_params(self) -> dict
        获取表格中的参数
    """
    def __init__(self, parent=None,):
        super().__init__(parent)

    def initUI(self, config, config_description):
        """初始化界面"""

        self.setWindowTitle("配置结果")

        screen_width = screen_size()[0]
        screen_height = screen_size()[1]

        self.myWidth = int(screen_width * 0.5)
        self.myHeight = int(screen_height * 0.6)
        self.setGeometry(int(screen_width) // 2 - int(self.myWidth) // 2,
                         int(screen_height) // 2 - int(self.myHeight) // 2,
                         self.myWidth, self.myHeight)

        try:
            self.mainLayout = QVBoxLayout()
            self.mainLayout.setContentsMargins(5, 5, 5, 5)

            self.first_tabs = QTabWidget()
            self.first_tabs_layout = QVBoxLayout()

            for key1 in config.keys():
                second_tabs = QTabWidget()
                second_tabs_layout = QVBoxLayout()

                dict1 = config[key1]

                tableWidget = QTableWidget()
                tableWidget.setRowCount(len(dict1))
                tableWidget.setColumnCount(3)
                tableWidget.setColumnWidth(0, 300)
                tableWidget.setColumnWidth(1, 300)
                tableWidget.setColumnWidth(2, 300)
                # tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

                headers = ["参数", "值", "描述"]
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
                    item.setFlags(item.flags() | Qt.ItemIsEditable)

                    item = QTableWidgetItem(config_description[key1][keys[i]])
                    item.setTextAlignment(Qt.AlignCenter)
                    tableWidget.setItem(i, 2, item)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                second_tabs_layout.addWidget(tableWidget)
                second_tabs.setLayout(second_tabs_layout)

                self.first_tabs_layout.addWidget(second_tabs)
                self.first_tabs.addTab(second_tabs, key1)

            self.mainLayout.addWidget(self.first_tabs)  # 添加第一层 QTabWidget 到主布局
            self.setLayout(self.mainLayout)
        except Exception as e:
            temp_str = "配置结果界面初始化失败！报错位置：ModifyConfigResultDialog.initUI()，错误信息：{}".format(e)
            print(temp_str)

    def get_table_params(self,) -> dict:
        """获取表格中的参数"""

        table_params = {}
        for i in range(self.first_tabs.count()):
            second_tabs = self.first_tabs.widget(i)
            tableWidget = second_tabs.layout().itemAt(0).widget()
            keys = [tableWidget.item(i, 0).text() for i in range(tableWidget.rowCount())]
            values = [tableWidget.item(i, 1).text() for i in range(tableWidget.rowCount())]
            table_params[self.first_tabs.tabText(i)] = dict(zip(keys, values))

        return table_params
