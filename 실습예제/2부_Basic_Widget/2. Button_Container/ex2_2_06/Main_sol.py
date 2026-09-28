import sys,subprocess
from PyQt5.QtWidgets import *

GUI_FILE_NAME = 'gui_sol'
subprocess.run([
    sys.executable,          
    '-m', 'PyQt5.uic.pyuic', 
    '-x', f'{GUI_FILE_NAME}.ui', 
    '-o', f'{GUI_FILE_NAME}.py'
])
from gui_sol import Ui_MainWindow


class Form(QMainWindow , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.year = '1학년'
        self.gender = '남자'
        self.setupUi(self)

        self.grpYear.buttonClicked.connect(self.getYear)
        self.grpGender.buttonClicked.connect(self.getGender)
        self.btnOK.clicked.connect(self.btnOK_Click)

    def getYear(self, radio):
        self.year = radio.text()

    def getGender(self, radio):
        self.gender = radio.text()

    def btnOK_Click(self):
        self.lblMsg.setText(f'{self.year} {self.gender} 입니다.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())



