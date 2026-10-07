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
        if role == Qt.DisplayRole:
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

    def n    (self, index):
        return len(self.contents[0])


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = None
        self.loadFile()
        self.model = TableModel(self.data)
        self.tableView.setModel(self.model)
        self.tableView.clicked.connect(lambda x: print(x.data()))

    def loadFile(self):
        with open('top2018.csv', 'r') as f:
            self.data = [line.split(',') for line in f.read().splitlines()]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
