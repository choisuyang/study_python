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

        self.btnPush.clicked.connect(self.btnPush_Clicked)
        self.btnPush.pressed.connect(self.btnPush_Pressed)
        self.btnPush.released.connect(self.btnPush_Released)
        self.btnPush.toggled.connect(self.btnPush_Toggled)

        self.btnCheckable.clicked.connect(self.btnCheckable_clicked)
        self.btnCheckable.toggled.connect(self.btnCheckable_Toggled)

    def btnPush_Toggled(self):
        print("btnPush_Toggled")

    def btnPush_Clicked(self, arg):
        print("btnPush_Clicked", arg)

    def btnPush_Pressed(self):
        print("btnPush_Pressed")

    def btnPush_Released(self):
        print("btnPush_Released")

    def btnCheckable_clicked(self, state):
        print("clicked state :", state)

    def btnCheckable_Toggled(self, state):
        print("toggled state :", state)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
