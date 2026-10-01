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
        self.cnt = 0
        self.instance_variable = 0
        self.lblState.setStyleSheet('background-color:red')
        self.btnPush.clicked.connect(self.Change_Color)
        self.btnToggle.toggled.connect(self.Toggle_color)
        

    def Change_Color(self):
        self.cnt += 1
        if (self.cnt == 1):
            self.lblColor.setStyleSheet('background-color:red')
        elif (self.cnt == 2):
            self.lblColor.setStyleSheet('background-color:green')
        elif (self.cnt == 3):
            self.lblColor.setStyleSheet('background-color:blue')
            self.cnt = 0


    def Toggle_color(self, state):
        if (state == True):
            self.btnToggle.setText("ON")
            self.lblState.setStyleSheet('background-color:green')
        else:
            self.btnToggle.setText("OFF")
            self.lblState.setStyleSheet('background-color:red')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
