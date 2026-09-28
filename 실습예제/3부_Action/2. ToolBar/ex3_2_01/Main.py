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
        self.setActionConnect()

    def setActionConnect(self):
        self.action_New.triggered.connect(self.newFile)
        self.action_Open.triggered.connect(self.openFile)
        self.action_Save.triggered.connect(self.saveFile)
        self.actionSave_As.triggered.connect(self.saveAsFile)
        self.action_Close.triggered.connect(self.exitProgram)

    def newFile(self):
        print('newFile')

    def openFile(self):
        print('openFile')

    def saveFile(self):
        print('saveFile')

    def saveAsFile(self):
        print('saveAsFile')

    def exitProgram(self):
        QApplication.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
