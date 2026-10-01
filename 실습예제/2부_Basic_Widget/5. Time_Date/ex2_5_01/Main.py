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
        self.tick = 0
        self.setupUi(self)

        self.tmr = QTimer(self)
        self.tmr.timeout.connect(self.func)
        self.lcdNumber.display(QTime.currentTime().toString('HH:mm:ss'))
        self.tmr.start(1000)
        self.lblGreen.setStyleSheet('background-color:green')
        self.lblRed.setStyleSheet('background-color:black')
        
    def func(self):
        self.tick +=1
        t = QTime.currentTime().toString("HH:mm:ss")
        self.lcdNumber.display(t)
        if self.tick % 2 == 0:
            self.lblGreen.setStyleSheet('background-color:green')
            self.lblRed.setStyleSheet('background-color:black')
        else:
            self.lblGreen.setStyleSheet('background-color:black')
            self.lblRed.setStyleSheet('background-color:red')
        print("*")
        
        # print(self.QTime.currentTime().toString('HH:mm:ss'))
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
