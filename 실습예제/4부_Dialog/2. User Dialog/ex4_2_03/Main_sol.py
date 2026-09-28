import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

MAIN_FILE_NAME = 'main_wnd'
DIALOG_FILE_NAME = 'dialog'
os.system('python -m PyQt5.uic.pyuic -x ' + MAIN_FILE_NAME + '.ui -o ' + MAIN_FILE_NAME + '.py')
os.system('python -m PyQt5.uic.pyuic -x ' + DIALOG_FILE_NAME + '.ui -o ' + DIALOG_FILE_NAME + '.py')
from main_wnd import Ui_MainWindow
from dialog import Ui_Dialog


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionHobby.triggered.connect(self.show_dialog)

    def show_dialog(self):
        dlg = dlgForm(self, name=self.editName.text())
        dlg.accepted.connect(lambda: self.print_info(dlg.getInfo()))
        dlg.open()

    def print_info(self, tinfo):
        self.lblNick.setText('닉네임: ' + tinfo[0] if tinfo[0] else '없음')
        self.lblHobby.setText('취미: ' + ",".join(tinfo[1]) if tinfo[1] else '없음')
        self.lblGender.setText('성별: ' + tinfo[2])


class dlgForm(QDialog, Ui_Dialog):

    def __init__(self, parent=None, flag=Qt.Dialog, name=None):
        super().__init__(parent, flag)
        self.setupUi(self)
        self.editNick.setText(name)

    def getNick(self):
        return self.editNick.text()

    def getHobby(self):
        lst_hobby = [chkbox.text() for chkbox in self.buttonGroup.buttons() if chkbox.isChecked()]
        # lst_hobby = []
        # for chkbox in self.buttonGroup.buttons():
        #     if chkbox.isChecked(): lst_hobby.append(chkbox.text())
        return lst_hobby

    def getGender(self):
        if self.rdoMale.isChecked():
            return '남자'
        else:
            return '여자'

    def getInfo(self):
        r = self.getNick(), self.getHobby(), self.getGender()
        return r


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
