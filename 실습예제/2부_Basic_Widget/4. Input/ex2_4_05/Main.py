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
        self.btnApply.clicked.connect(self.applyClicked)

    def applyClicked(self):
        font = self.cboFont.currentFont()
        font.setPointSize(int(self.linFontSize.text())if self.linFontSize.text() != '' else font.pointSize())
        font.setBold(self.chkBold.isChecked())
        font.setItalic(self.chkItalic.isChecked())
        self.lblEng.setFont(font)
        self.lblKor.setFont(font)
        self.lblEng.adjustSize()
        self.lblKor.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
