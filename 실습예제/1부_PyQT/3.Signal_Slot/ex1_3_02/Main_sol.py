import sys, subprocess
from PyQt5.QtWidgets import *

GUI_FILE_NAME = 'gui_sol'
subprocess.run([
    sys.executable,          
    '-m', 'PyQt5.uic.pyuic', 
    '-x', f'{GUI_FILE_NAME}.ui', 
    '-o', f'{GUI_FILE_NAME}.py'
])

from gui_sol import Ui_MainWindow


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnHello.clicked.connect(self.print_hello)
        self.btnWorld.clicked.connect(self.print_world)

    def print_hello(self):
        self.lblMsg.setText("Hello")

    def print_world(self):
        self.lblMsg.setText("World")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
