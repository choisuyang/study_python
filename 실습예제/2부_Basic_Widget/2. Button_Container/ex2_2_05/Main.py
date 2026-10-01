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

        self.btnOK.clicked.connect(self.btnOK_Click)

    def btnOK_Click(self):
        obj = self.findChildren(QCheckBox)
        l = []
        for chk in obj:
            if chk.isChecked():
                l.append(chk.text())
        if l:
            self.lblMsg.setText(f'나는 {",".join(l)}언어 사용 가능')
        else:
            self.lblMsg.setText('나는 사용 할수 있는 언어 없음')

        # todo : 코드를 구현하라 
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
