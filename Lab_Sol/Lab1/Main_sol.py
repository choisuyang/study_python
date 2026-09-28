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
        self.cnt = 0
        self.setupUi(self)
        self.btnPush.clicked.connect(self.Chage_Color)
        self.btnToggle.toggled.connect(self.Operation)
        self.lblState.setStyleSheet('background-color: red')

    def Chage_Color(self):
        color = ['red', 'green', 'blue']
        self.lblColor.setStyleSheet('background-color: ' + color[self.cnt % 3])
        self.lblColor.setText(color[self.cnt % 3])
        self.cnt = self.cnt + 1

    def Operation(self, state):
        self.btnToggle.setText('ON' if state else 'OFF')
        self.lblState.setStyleSheet('background-color: ' + ('green' if state else 'red'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
