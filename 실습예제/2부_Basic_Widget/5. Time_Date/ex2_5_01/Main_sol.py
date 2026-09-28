import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

GUI_FILE_NAME = 'gui'
os.system('python -m PyQt5.uic.pyuic -x ' + GUI_FILE_NAME + '.ui -o ' + GUI_FILE_NAME + '.py')

from gui import Ui_MainWindow


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.tick = 0
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeTick)
        self.lcdNumber.display(QTime.currentTime().toString('HH:mm:ss'))
        self.timer.start(1000)

        self.lblRed.setStyleSheet('background-color: red')
        self.lblGreen.setStyleSheet('background-color: black')

    def timeTick(self):
        strtime = QTime().currentTime().toString('HH:mm:ss')
        self.lcdNumber.display(strtime)
        if self.tick % 2:
            self.lblRed.setStyleSheet('background-color: red')
            self.lblGreen.setStyleSheet('background-color: black')
        else:
            self.lblRed.setStyleSheet('background-color: black')
            self.lblGreen.setStyleSheet('background-color: green')
        self.tick = self.tick + 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
