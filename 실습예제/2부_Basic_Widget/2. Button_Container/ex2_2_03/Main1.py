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
        self.lang = ''
        self.setupUi(self)

        self.lblMsg.setText('나는 사용할 수 있는 언어가 없다')

        self.chkTri.stateChanged.connect(self.chkTri_stateChanged)
        self.chkTri.toggled.connect(self.chkTri_toggled)

        self.chkC.toggled.connect(self.Use_Lang)
        self.chkCpp.toggled.connect(self.Use_Lang)
        self.chkJava.toggled.connect(self.Use_Lang)
        self.chkPython.toggled.connect(self.Use_Lang)

    def chkTri_stateChanged(self, arg):
        print('state changed', arg)
        print('checkState()', self.chkTri.checkState())
        print('isChecked()', self.chkTri.isChecked())
        print()

    def chkTri_toggled(self, arg):
        print('toggled', arg)

    def Use_Lang(self):
        # Todo : 코드를 작성하시오
        result = ''
        if self.chkC.isChecked(): result+= 'C, '
        if self.chkCpp.isChecked(): result+= 'Cpp, '
        if self.chkJava.isChecked(): result+= 'Java, '
        if self.chkPython.isChecked(): result+= 'Pyhon, '
        if not result :
            self.lblMsg.setText('나는 사용할수잇는 언어 없음')
        else:
            self.lblMsg.setText(f'나는 {result[:-2]} 언어 사용 가능')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
