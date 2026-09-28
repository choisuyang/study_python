import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tableModel import *

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
        self.model = None
        self.btnOpen.clicked.connect(self.loadFile)


    def loadFile(self):
        with open('ramen.csv', 'r') as f:
            data = [line.split(',') for line in f.read().splitlines()]
            self.model = TableModel(data)
            self.tableView.setModel(self.model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
