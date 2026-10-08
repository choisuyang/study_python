import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

MAIN_FILE_NAME = 'main_wnd'
DIALOG_FILE_NAME = 'dialog'
subprocess.run([
    sys.executable,          
    '-m', 'PyQt5.uic.pyuic', 
    '-x', f'{MAIN_FILE_NAME}.ui', 
    '-o', f'{MAIN_FILE_NAME}.py'
])
subprocess.run([
    sys.executable,          
    '-m', 'PyQt5.uic.pyuic', 
    '-x', f'{DIALOG_FILE_NAME}.ui', 
    '-o', f'{DIALOG_FILE_NAME}.py'
])
from main_wnd import Ui_MainWindow
from dialog import Ui_Dialog


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionHobby.triggered.connect(self.show_dialog)

    def show_dialog(self):
        # todo : dlgForm 객체를 생성하여 이름을 넘겨주어 객체 생성
        dlg = dlgForm(name = self.editName.text()) # Todo : 생성자 수정
        dlg.open()
        dlg.accepted.connect(lambda: self.print_info(dlg.getInfo()))

        # r = dlg.exec()
        # if r == QDialog.Accepted:
        #     tinfo = dlg.getInfo()
        #     self.print_info(tinfo)
        # dlg.accepted.connect(lambda: self.print_info(dlg.getInfo()))
        # dlg.open()

    def print_info(self, tinfo):
        # Todo : 다이얼로그에서 넘겨 받은 tinfo를 main window에 표시
        self.lblNick.setText('닉네임 : ' + tinfo[0] if tinfo[0] else '닉네임 : ')
        self.lblHobby.setText('취미 : ' + ', '.join(tinfo[1]) if tinfo[1] else '취미 : ')
        self.lblGender.setText('성별 : ' + tinfo[2] if tinfo[2] else '성별 : ')


class dlgForm(QDialog, Ui_Dialog):

    def __init__(self, parent=None, flag=Qt.Dialog, name=None):
        super().__init__(parent, flag)
        self.setupUi(self)
        # Todo :  넘어온 name를 line edit에 표시
        self.editNick.setText(name)

    def getNick(self):
        # Todo : 닉네임 리턴
        nick_name = self.editNick.text()
        return nick_name

    def getHobby(self):
        # Todo : 선택된 취미를 list로 만들어 리턴
        lst_hobby = []
        for chkbox in self.buttonGroup.buttons():
            if chkbox.isChecked():
                lst_hobby.append(chkbox.text())
        return lst_hobby

    # def getGender(self):
    #     # Todo : 선택된 성별을 문자열로 리턴
        
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
