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
        self.idpass = {'AXQ1000': '123456', 'AXQ1001': '123456', 'AXQ1002': '123456', 'AXQ1003': '123456','AXQ1004': '123456'}
        self.btnOK.clicked.connect(self.Confirm_Password)
        self.btnChange.clicked.connect(self.Change_Password)

    def Confirm_Password(self):
        if not self.Check_Validation():
            return
        if self.linID.text() not in self.idpass:
            self.lblMsg.setText('없는 아이디 입니다')
        elif self.idpass[self.linID.text()] != self.linPass.text():
            self.lblMsg.setText('비밀번호가 틀렸습니다')
        else:
            self.lblMsg.setText('인증되었습니다')

    def Change_Password(self):
        if not self.Check_Validation():
            return
        if self.linID.text() not in self.idpass:
            self.lblMsg.setText('없는 아이디 입니다')
        else:
            self.idpass[self.linID.text()] = self.linPass.text()
            self.lblMsg.setText(f'비밀번호 변경 : [{self.linPass.text()}]')

    def Check_Validation(self):
        for wid in self.findChildren(QLineEdit):
            if not wid.hasAcceptableInput():
                item = self.formLayout.labelForField(wid).text()
                self.lblMsg.setText(f'{item}를 입력해 주세요')
                return False
            else:
                self.lblMsg.setText('유효한 데이터 입니다')
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
