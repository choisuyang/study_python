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
        self.btngetText.clicked.connect(self.getText)
        self.btngetTextMulti.clicked.connect(self.getTextMulti)
        self.btngetInt.clicked.connect(self.getInt)
        self.btngetDouble.clicked.connect(self.getDouble)
        self.btngetItem.clicked.connect(self.getItem)

    def getText(self):
        r, ok = QInputDialog.getText(self, "getText", "이름을 입력 하세요")
        print(r, ok)
        if ok:
            # 입력받은 내용 출력
            self.lblgetText.setText('')
            self.lblgetText.adjustSize()

    def getTextMulti(self):
        r, ok = QInputDialog.getMultiLineText(self, "getMultiLineText", "메시지를 입력하세요")
        print(r, ok)
        if ok:
            # 입력받은 내용 출력
            self.lblgetTextMulti.setText('')
            self.lblgetTextMulti.adjustSize()

    def getInt(self):
        r, ok = QInputDialog.getInt(self, "getInt", "나이를 입력하세요", min=0, max=200)
        print(r, ok)
        if ok:
            # 입력받은 내용 출력
            self.lblgetInt.setText('')
            self.lblgetInt.adjustSize()

    def getDouble(self):
        r, ok = QInputDialog.getDouble(self, "getDouble", "키(cm)를 입력하세요", decimals=2, min=0.0, max=300.0)
        print(r, ok)
        if ok:
            # 입력받은 내용 출력
            self.lblgetInt.setText('')
            self.lblgetInt.adjustSize()

    def getItem(self):
        l = ['등산', '낚시', '캠핑', '게임', '독서', '음악감상']
        r, ok = QInputDialog.getItem(self, "getItem", "취미를 고르세요", l, current=5)
        print(r, ok)
        if ok:
            # 입력받은 내용 출력
            self.lblgetItem.setText('')
            self.lblgetItem.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
