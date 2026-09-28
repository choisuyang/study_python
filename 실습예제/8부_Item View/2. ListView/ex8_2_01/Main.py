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


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        data = ['item1', 'item2', 'item3', 'item4', 'item5']
        self.model = QStringListModel(data)
        self.listView.setModel(self.model)
        self.comboBox.setModel(self.model)

        self.btnAdd.clicked.connect(self.addData)
        self.btnInsert.clicked.connect(self.insertData)
        self.btnDelete.clicked.connect(self.deleteData)
        self.model.dataChanged.connect(self.dataChange)

    def dataChange(self, index):
        print('data changed:', index.data())

    def addRow(self, row):
        if not self.lineEdit.text():
            return
        self.model.insertRow(row)
        index = self.model.index(row)
        self.model.setData(index, self.lineEdit.text())
        self.listView.setCurrentIndex(index)

    def addData(self):
        row = self.model.rowCount()
        self.addRow(row)

    def insertData(self):
        row = self.listView.currentIndex().row()
        self.addRow(row)

    def deleteData(self):
        self.model.removeRow(self.listView.currentIndex().row())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
