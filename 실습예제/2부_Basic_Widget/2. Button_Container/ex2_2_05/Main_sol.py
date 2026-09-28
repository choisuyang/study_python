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
        use_lang = []

        # comprehension 사용한 예
        # use_lang = [chkbox.text() for chkbox in self.groupBox.findChildren(QCheckBox) if chkbox.isChecked()]

        # 반복문을 사용한 예
        for chkbox in self.groupBox.findChildren(QCheckBox):
            if chkbox.isChecked(): use_lang.append(chkbox.text())

        if len(use_lang) == 0:
            self.lblMsg.setText('나는 사용할 수 있는 언어가 없다')
        else:
            self.lblMsg.setText(f'나는 {", ".join(use_lang)} 언어를 사용할 수 있다')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
