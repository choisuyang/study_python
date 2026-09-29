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
        self.text = ''
        self.buttonGroup.buttonClicked.connect(self.funcCal)
        self.buttonGroup_2.buttonClicked.connect(self.funcCal2)

    def funcCal(self, a):
        self.text = self.text + a.text()
        self.label.setText(self.text)

    
    def funcCal2(self,b):
        if b.text() == "=":
            # self.text = (str(eval(self.text)))
            self.label.setText(str(eval(self.text)))
        elif b.text() =="C":
            self.label.setText('')
            self.text = ''
        elif b.text() == "<-":
            self.text = self.text[0:-1]
            self.label.setText(self.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
