import sys, subprocess
from PyQt5.QtWidgets import *

from PyQt5 import uic

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

        self.btnPush.clicked.connect(self.btnPush_clicked)
        self.btnDisable.clicked.connect(self.btnDisable_clicked)
        self.btnFlat.clicked.connect(self.btnFlat_clicked)
        self.btnCheckable.clicked.connect(self.btnCheckable_clicked)
        self.btnAutoRepeat.clicked.connect(self.btnAutoRepeat_clicked)
        self.btnDefault.clicked.connect(self.btnDefault_clicked)

    def btnPush_clicked(self):
        print("btnPush_clicked")

    def btnDisable_clicked(self):
        print("btnDisable_clicked")

    def btnFlat_clicked(self):
        print("btnFlat_clicked")

    def btnCheckable_clicked(self):
        print("btnCheckable_clicked")

    def btnAutoRepeat_clicked(self):
        print("btnAutoRepeat_clicked")

    def btnDefault_clicked(self):
        print("btnDefault_clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
