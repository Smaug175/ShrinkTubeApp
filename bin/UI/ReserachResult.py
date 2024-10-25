import os

from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QDialog, QHBoxLayout, \
    QAbstractItemView, \
    QToolBar, QComboBox, QLabel, QPushButton, QTableView, QHeaderView

os.environ['QT_SCALE_FACTOR'] = '1.1'

import pandas as pd
import json


def screen_size():
    """获取屏幕尺寸"""
    screen = QApplication.desktop().screenGeometry()
    return screen.width(), screen.height()


class ReserachResultDialog(QDialog):
    """搜索结果的显示界面

    Methods
    _______
    initUI(self, result)
        初始化界面
    """

    def __init__(self, parent=None,):
        super().__init__(parent)

    def initUI(self, result):
        self.setWindowTitle("搜索结果")

        screen_width = screen_size()[0]
        screen_height = screen_size()[1]

        self.myWidth = int(screen_width * 0.8)
        self.myHeight = int(screen_height * 0.6)
        self.setGeometry(int(screen_width) // 2 - int(self.myWidth) // 2,
                         int(screen_height) // 2 - int(self.myHeight) // 2,
                         self.myWidth, self.myHeight)

        # 导入参数描述
        with open('bin/model/Normal/Parameter_Description.json', 'r', encoding='utf-8') as file:
            Parameter_Description = json.load(file)
        with open('bin/model/Normal/Parameter_Calculate_Method.json', 'r', encoding='utf-8') as file:
            Parameter_Calculate_Method = json.load(file)

        try:
            self.mainLayout = QVBoxLayout()
            self.mainLayout.setContentsMargins(5, 5, 5, 5)

            first_tabs = QTabWidget()
            first_tabs_layout = QVBoxLayout()

            for key1 in result.keys():
                second_tabs = QTabWidget()
                second_tabs_layout = QVBoxLayout()

                dict1 = result[key1]

                for key2 in dict1.keys():
                    third_tabs = QTabWidget()
                    third_tabs_layout = QHBoxLayout()

                    dict2 = dict1[key2]
                    tableWidget = QTableWidget()
                    tableWidget.setRowCount(len(dict2))
                    tableWidget.setColumnCount(4)
                    tableWidget.setColumnWidth(1, 300)
                    tableWidget.setColumnWidth(2, 300)
                    tableWidget.setColumnWidth(3, 800)
                    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

                    headers = ["参数", "值", "描述", "计算方法"]
                    tableWidget.setHorizontalHeaderLabels(headers)

                    keys = list(dict2.keys())
                    for i in range(len(keys)):
                        item = QTableWidgetItem(keys[i])
                        item.setTextAlignment(Qt.AlignCenter)
                        tableWidget.setItem(i, 0, item)

                        item = QTableWidgetItem(str(dict2[keys[i]]))
                        item.setTextAlignment(Qt.AlignCenter)
                        tableWidget.setItem(i, 1, item)

                        if len(key2) > 6:  # 使用图号的关键字作为key1
                            temp = key2[:-4]
                        else:
                            temp = key2

                        item = QTableWidgetItem(Parameter_Description[temp][keys[i]])
                        item.setTextAlignment(Qt.AlignCenter)
                        tableWidget.setItem(i, 2, item)

                        item = QTableWidgetItem(Parameter_Calculate_Method[temp][keys[i]])
                        item.setTextAlignment(Qt.AlignCenter)
                        tableWidget.setItem(i, 3, item)

                    third_tabs_layout.addWidget(tableWidget)
                    third_tabs.setLayout(third_tabs_layout)

                    second_tabs_layout.addWidget(third_tabs)
                    second_tabs.addTab(third_tabs, key2)

                first_tabs_layout.addWidget(second_tabs)
                first_tabs.addTab(second_tabs, key1)

            self.mainLayout.addWidget(first_tabs)  # 添加第一层 QTabWidget 到主布局
            self.setLayout(self.mainLayout)
        except Exception as e:
            print(e)

class ReserachResultDialog_Mold(QDialog):
    """模具的搜索结果的显示界面

    Methdos
    _______
    initUI(self, crypto_data_instance)
        初始化界面
    search(self)
        搜索模具
    """

    def __init__(self, parent=None,):
        super().__init__(parent)

    def initUI(self, crypto_data_instance):
        self.setWindowTitle("搜索结果")
        self.crypto_data_instance = crypto_data_instance

        screen_width = screen_size()[0]
        screen_height = screen_size()[1]

        self.myWidth = int(screen_width * 0.7)
        self.myHeight = int(screen_height * 0.6)
        self.setGeometry(int(screen_width) // 2 - int(self.myWidth) // 2,
                         int(screen_height) // 2 - int(self.myHeight) // 2,
                         self.myWidth, self.myHeight)
        big_name = [
            "DC0124",
            "DC0121",
            "DC0125"
        ]

        DC0124_name = [
            "AD03",
            "DIEO",
            "SS01",
            "AD02",
            "ADIE",
            "ADBT",
            "AD01"
        ] # 默认显示的模具名称

        self.mainLayout = QVBoxLayout()

        toolbar = QToolBar('工具栏')
        toolbar_layout = toolbar.layout()
        toolbar_layout.setSpacing(10)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)

        label0 = QLabel('选择机器型号：')
        self.comboBox0 = QComboBox(self)
        self.comboBox0.setFixedWidth(100)
        self.comboBox0.addItems(big_name)
        self.comboBox0.activated[str].connect(self._name_changed_)  # 点击下拉框触发事件

        label = QLabel('选择模具：')

        self.comboBox = QComboBox(self)
        self.comboBox.setFixedWidth(100)
        self.comboBox.addItems(DC0124_name)

        btn = QPushButton('搜索')
        btn.clicked.connect(self.search)

        toolbar.addWidget(label0)
        toolbar.addWidget(self.comboBox0)
        toolbar.addWidget(label)
        toolbar.addWidget(self.comboBox)
        toolbar.addWidget(btn)

        # 将工具栏添加到窗口顶部
        self.mainLayout.addWidget(toolbar)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)

        result = self.crypto_data_instance.query_all_mold_by_mold_name(self.comboBox0.currentText()+'-'+self.comboBox.currentText())

        # 创建 DataFrame
        df = pd.DataFrame(list(result.values()))

        # 创建模型
        self.model = DataFrameModel(df)

        # 创建表格视图
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列等比例扩展

        self.mainLayout.addWidget(self.tableView)
        self.setLayout(self.mainLayout)

    def _name_changed_(self, text):
        """下拉框选项改变时触发的事件"""
        machine_name = self.comboBox0.currentText()
        DC0124_name = [
            "AD03",
            "DIEO",
            "SS01",
            "AD02",
            "ADIE",
            "ADBT",
            "AD01"
        ]
        DC0121_name = [
            "AD03",
            "AD04",
            "DIEO",
            "SS01",
            "AD02",
            "ADIE",
            "ADBT",
            "AD01"
        ]
        DC0125_name = [
            "AD06",
            "AD07",
            "DIEO",
            "SS01",
            "ADIE",
            "ADBT",
        ]

        if machine_name == "DC0124":
            self.comboBox.clear()
            self.comboBox.addItems(DC0124_name)
        elif machine_name == "DC0121":
            self.comboBox.clear()
            self.comboBox.addItems(DC0121_name)
        elif machine_name == "DC0125":
            self.comboBox.clear()
            self.comboBox.addItems(DC0125_name)


    def search(self):
        """搜索模具"""
        if self.comboBox0.currentText() == 'DC0125' and self.comboBox.currentText() == 'AD06':
            # 由于AD06模具有两个版本，所以需要特殊处理
            mold_name = self.comboBox0.currentText() + '-' + self.comboBox.currentText() + '_S'
        else:
            mold_name = self.comboBox0.currentText() + '-' + self.comboBox.currentText()
        result = self.crypto_data_instance.query_all_mold_by_mold_name(mold_name)
        df = pd.DataFrame(list(result.values()))
        self.model = DataFrameModel(df)
        self.tableView.setModel(self.model)

class DataFrameModel(QAbstractTableModel):
    """一个自定义的模型，用于将 DataFrame 转换为 QTableView 可以显示的格式

    Methods
    _______
    rowCount(self, parent=None) -> int
        返回行数
    columnCount(self, parent=None) -> int
        返回列数
    data(self, index, role=Qt.DisplayRole)
        返回指定索引的数据
    headerData(self, section, orientation, role=Qt.DisplayRole)
        返回表头数据
    """

    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent=None) -> int:
        """返回行数"""
        return len(self.data)

    def columnCount(self, parent=None) -> int:
        """返回列数"""
        return len(self.data.columns)

    def data(self, index, role=Qt.DisplayRole):
        """返回指定索引的数据"""

        if role == Qt.DisplayRole:
            return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """返回表头数据"""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.data.columns[section]
            else:
                return self.data.index[section]