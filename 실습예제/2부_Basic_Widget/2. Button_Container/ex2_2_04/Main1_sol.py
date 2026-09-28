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
        self.lang = []
        self.setupUi(self)

        self.lblMsg.setText('나는 사용할 수 있는 언어가 없다')

        self.chkTri.stateChanged.connect(self.chkTri_stateChanged)
        self.chkTri.toggled.connect(self.chkTri_toggled)

        self.buttonGroup.buttonClicked.connect(self.Use_Lang)

    def chkTri_stateChanged(self, arg):
        print('state changed', arg)
        print('checkState()', self.chkTri.checkState())
        print('isChecked()', self.chkTri.isChecked())
        print()

    def chkTri_toggled(self, arg):
        print('toggled', arg)

    def Use_Lang(self, chkbox):

        if chkbox.isChecked():
            self.lang.append(chkbox.text())
        else:
            self.lang.remove(chkbox.text())

        #self.lang.sort()
        if len(self.lang) == 0:
            self.lblMsg.setText('나는 사용할 수 있는 언어가 없다')
        else:
            self.lblMsg.setText(f'나는 {", ".join(self.lang)} 언어를 사용할 수 있다')
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
