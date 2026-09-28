import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

GUI_FILE_NAME = 'gui'
subprocess.run([
    sys.executable,          
    '-m', 'PyQt5.uic.pyuic', 
    '-x', f'{GUI_FILE_NAME}.ui', 
    '-o', f'{GUI_FILE_NAME}.py'
])

from gui import Ui_MainWindow


class TableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self.contents = data or []

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.contents[index.row() + 1][index.column()]
        return QVariant()

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return self.contents[0][section]
        else:
            return section + 1

    def rowCount(self, index):
        return len(self.contents) - 1

    def columnCount(self, index):
        return len(self.contents[0])


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = None
        self.loadFile()

        self.proxy_model = QSortFilterProxyModel()
        self.model = TableModel(self.data)
        self.proxy_model.setSourceModel(self.model)
        self.tableView.setModel(self.proxy_model)
        self.pushButton.clicked.connect(self.clearFilter)
        self.tabWidget.tabBarClicked.connect(self.regexFilter)
        self.makeComboData()

        self.cboBrand.currentIndexChanged.connect(lambda: self.fixedStingFilter(1))
        self.cboCountry.currentIndexChanged.connect(lambda: self.fixedStingFilter(4))

    def makeComboData(self):
        # self.cboBrand.setModel(self.proxy_model)
        # self.cboBrand.setModelColumn(1)
        # self.cboCountry.setModel(self.proxy_model)
        # self.cboCountry.setModelColumn(4)

        trans = list(map(set, zip(*self.model.contents[1:])))
        self.cboBrand.addItems(sorted(list(trans[1])))
        self.cboCountry.addItems(sorted(list(trans[4])))

    def fixedStingFilter(self, mode):
        if mode == 1:
            filter_string = self.cboBrand.currentText()
        else:
            filter_string = self.cboCountry.currentText()
        self.proxy_model.setFilterFixedString(filter_string)
        self.proxy_model.setFilterKeyColumn(mode)

    def regexFilter(self, index):
        groups = ['A-C', 'D-F', 'G-I', 'J-L', 'M-O', 'P-R', 'S-U', 'VW', 'X-Z']
        exp = '^[{}].*'.format(groups[index])
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterRegExp(exp)
        self.proxy_model.setFilterKeyColumn(1)

    def clearFilter(self):
        self.proxy_model.setFilterRegExp('')
        self.proxy_model.setFilterKeyColumn(1)

    def loadFile(self):
        with open('ramen.csv', 'r') as f:
            self.data = [line.split(',') for line in f.read().splitlines()]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
