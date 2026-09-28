import sys, subprocess
from PyQt5.QtWidgets import *

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
from PyQt5.QtCore import Qt


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.show_Dialog)

    def show_Dialog(self):
        dlg = dlgForm(self)
        dlg.accepted.connect(self.dlg_accept)
        dlg.rejected.connect(self.dlg_reject)
        r = dlg.exec()

    def dlg_accept(self):
        print('accepted')

    def dlg_reject(self):
        print('reject')


class dlgForm(QDialog, Ui_Dialog):
    def __init__(self, parent=None, flag=Qt.Dialog):
        super().__init__(parent, flag)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.dlg_accepted)
        self.buttonBox.rejected.connect(self.dlg_rejected)
        self.buttonBox.helpRequested.connect(self.dlg_help)
        self.buttonBox.clicked.connect(self.dlg_clicked)
        self.btnAction1 = self.buttonBox.addButton('action1', QDialogButtonBox.ActionRole)
        self.btnAction2 = self.buttonBox.addButton('action2', QDialogButtonBox.ActionRole)

    def dlg_accepted(self):
        print('dialog accepted')

    def dlg_rejected(self):
        print('dialog rejected')

    def dlg_help(self):
        QMessageBox.information(self, "도움말", "도움말을 표시합니다.", QMessageBox.Ok)

    def dlg_clicked(self, btn):
        if btn == self.btnAction1:
            print('action 1')
        elif btn == self.btnAction2:
            print('action 2')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
