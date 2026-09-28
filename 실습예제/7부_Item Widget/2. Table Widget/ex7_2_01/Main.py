import sys, subprocess
from PyQt5.QtWidgets import *

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
        self.data = []

        self.btnLoad.clicked.connect(self.loadFile)
        self.btnSave.clicked.connect(self.saveFile)
        self.btnAddRow.clicked.connect(self.addRow)
        self.btnAddRow.setEnabled(False)
        self.btnSave.setEnabled(False)

    def addRow(self):
        name = self.nameLineEdit.text()
        kor = self.korLineEdit.text()
        eng = self.engLineEdit.text()
        mat = self.matLineEdit.text()
        self.data.append([name, kor, eng, mat])
        self.tableWidget.setRowCount(len(self.data) - 1)
        r = self.tableWidget.rowCount() - 1
        for c, cell in enumerate(self.data[-1]):
            self.tableWidget.setItem(r, c, QTableWidgetItem(cell))
        self.tableWidget.resizeRowsToContents()

    def loadFile(self):
        with open('data.csv', 'r') as f:
            lines = f.readlines()
        self.data = [l.rstrip().split(',') for l in lines if len(l.rstrip()) != 0]
        self.btnAddRow.setEnabled(True)
        self.btnSave.setEnabled(True)
        self.make_table()

    def saveFile(self):
        lines = [','.join(line) + '\n' for line in self.data]
        with open('data.csv', 'w') as f:
            f.writelines(lines)

    def make_table(self):
        self.tableWidget.setRowCount(len(self.data) - 1)
        self.tableWidget.setColumnCount(len(self.data[0]))
        hlabel = self.data[0]
        self.tableWidget.setHorizontalHeaderLabels(hlabel)

        for r, record in enumerate(self.data[1::]):
            for c, cell in enumerate(record):
                self.tableWidget.setItem(r, c, QTableWidgetItem(cell))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
