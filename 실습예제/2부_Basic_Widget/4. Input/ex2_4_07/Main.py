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
        self.dialR.valueChanged.connect(self.changeColor)
        self.dialG.valueChanged.connect(self.changeColor)
        self.dialB.valueChanged.connect(self.changeColor)


    def changeColor(self):
        back_color = f'rgb({self.dialR.value()}, {self.dialG.value()}, {self.dialB.value()})'
        fore_color = f'rgb({self.dialR.value() ^ 255}, {self.dialG.value() ^ 255, {self.dialB.value() ^255}})'
        self.lblColor.setStyleSheet(f'background-color: {back_color};color:{fore_color}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
