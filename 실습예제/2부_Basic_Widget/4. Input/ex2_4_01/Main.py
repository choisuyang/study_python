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

        self.linIn.editingFinished.connect(self.linIn_editingFinished)
        self.linIn.returnPressed.connect(self.linIn_returnPressed)
        self.linIn.textChanged.connect(self.linIn_textChanged)
        self.linIn.textEdited.connect(self.linIn_textEdited)
        self.btnSet.clicked.connect(self.btnSet_clicked)
        self.btnDisp.clicked.connect(self.btnDisp_clicked)
        self.btnText.clicked.connect(self.btnText_clicked)
        self.radioEcho.buttonClicked.connect(self.change_Echo)

    def linIn_editingFinished(self):
        print('editingFinished', self.linIn.text())

    def linIn_returnPressed(self):
        print('returnPressed', self.linIn.text())

    def linIn_textChanged(self, arg):
        print('textChanged', arg)

    def linIn_textEdited(self, arg):
        print('textEdited', arg)

    def btnSet_clicked(self):
        self.linIn.setText(self.linSet.text())

    def btnDisp_clicked(self):
        self.lblMsg1.setText(self.lineEdit.displayText())

    def btnText_clicked(self):
        self.lblMsg2.setText(self.lineEdit.text())

    def change_Echo(self, radiobtn):
        if radiobtn == self.radioPass:
            self.lineEdit.setEchoMode(QLineEdit.Password)
        else:
            self.lineEdit.setEchoMode(QLineEdit.NoEcho)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
