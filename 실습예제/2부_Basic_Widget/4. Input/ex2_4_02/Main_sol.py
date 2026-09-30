import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

GUI_FILE_NAME = 'gui_sol'
subprocess.run([
    sys.executable,          
    '-m', 'PyQt5.uic.pyuic', 
    '-x', f'{GUI_FILE_NAME}.ui', 
    '-o', f'{GUI_FILE_NAME}.py'
])
from PyQt5.QtCore import QRegExp
from gui_sol import Ui_MainWindow


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnOK.clicked.connect(self.btnOK_click)
        self.LineEdit_3.setValidator(QIntValidator(0, 100, self))
        self.LineEdit.setValidator(QDoubleValidator(0.0, 100.0, 2, self))
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        self.linIP.setValidator(QRegExpValidator(ipRegex, self))

    def btnOK_click(self):
        item = ['아이디', '전화번호', '국어점수', '백분위', '비밀번호', 'IP']
        for i, wid in enumerate(self.findChildren(QLineEdit)):
            if not wid.hasAcceptableInput():
                self.lblError.setText(f'{item[i]}항목 오류입니다.')
                wid.setFocus()
                
                break
        else:
            self.lblError.setText('모두 정상입니다.')

        # for wid in self.findChildren(QLineEdit):
        #     if not wid.hasAcceptableInput():
        #          self.lblError.setText(f'{self.formLayout.labelForField(wid).text()}항목 오류입니다.')
        #         wid.setFocus()
        #         break
        # else:
        #     self.lblError.setText('모두 정상입니다.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
