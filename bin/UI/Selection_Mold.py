from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem, QVBoxLayout,\
    QLabel

class ComboCheckBox(QComboBox):
    """选择模具的组合框，可以多选，使用QCheckBox作为下拉列表的项

    Methods
    _______
    initUI(self) -> None
        初始化界面
    addItems(self, items: list) -> None
        添加项
    onItemChanged(self) -> None
        当QCheckBox的状态改变时，更新组合框的文本
    getSelectedItems(self) -> list
        返回当前选中的项
    selectAll(self) -> None
        全选
    clearItems(self) -> None
        清空所有项
    """
    def __init__(self, items=[], parent=None):
        """初始化"""
        super(ComboCheckBox, self).__init__(parent)
        self.items = items
        self.initUI()

    def initUI(self):
        """初始化界面"""

        # 设置组合框为可编辑，并使用自定义的QLineEdit
        self.setEditable(True)
        self.lineEdit().setPlaceholderText("请选择需要计算的模具")
        self.lineEdit().setReadOnly(True)  # 设置为只读，以防止用户直接编辑

        # 创建QListWidget作为下拉列表
        self.listWidget = QListWidget()
        self.addItems(self.items)

        # 设置QListWidget作为组合框的视图
        self.setModel(self.listWidget.model())
        self.setView(self.listWidget)

        # 连接itemChanged信号到onItemChanged槽函数
        for i in range(self.listWidget.count()):
            item_widget = self.listWidget.itemWidget(self.listWidget.item(i))
            item_widget.stateChanged.connect(self.onItemChanged)

        # 默认全选
        self.selectAll()

    def addItems(self, items):
        """添加项"""

        # 将每个item都添加到QListWidget中，并用QCheckBox作为它的widget
        for item in items:
            listItem = QListWidgetItem(self.listWidget)
            checkBox = QCheckBox(item)
            checkBox.setChecked(True)  # 设置默认选中
            self.listWidget.setItemWidget(listItem, checkBox)

    def onItemChanged(self):
        """当QCheckBox的状态改变时，更新组合框的文本"""

        # 不再更新组合框文本框中显示的已选项，保持占位符文本不变
        pass

    def getSelectedItems(self) -> list:
        """返回当前选中的项"""

        selected_items = []
        for i in range(self.listWidget.count()):
            checkBox = self.listWidget.itemWidget(self.listWidget.item(i))
            if checkBox.isChecked():
                selected_items.append(checkBox.text())
        return selected_items

    def selectAll(self):
        """全选"""

        for i in range(self.listWidget.count()):
            checkBox = self.listWidget.itemWidget(self.listWidget.item(i))
            checkBox.setChecked(True)
        # 保持文本框内容不变，不再更新

    def clearItems(self):
        """清空所有项"""

        while self.listWidget.count():
            item = self.listWidget.takeItem(0)  # 取出并删除第一个项
            widget = self.listWidget.itemWidget(item)
            if widget:  # 如果存在关联的 widget，例如 QCheckBox，也删除它
                widget.deleteLater()
