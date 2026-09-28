import sys,subprocess
from PyQt5.QtWidgets import *

GUI_FILE_NAME = 'gui'
subprocess.run([
    sys.executable,          
    '-m', 'PyQt5.uic.pyuic', 
    '-x', f'{GUI_FILE_NAME}.ui', 
    '-o', f'{GUI_FILE_NAME}.py'
])
from gui import Ui_MainWindow


class Form(QMainWindow , Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.year = '1학년'
        self.gender = '남자'
        self.setupUi(self)

        self.btnOK.clicked.connect(self.btnOK_Click)
        # Todo : radio 버튼의 시그널 슬롯 연결


    def btnOK_Click(self):
        self.lblMsg.setText('{} {} 입니다.'.format(self.year, self.gender))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())



