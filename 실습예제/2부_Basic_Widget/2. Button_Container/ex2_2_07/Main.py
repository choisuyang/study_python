import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

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

        self.lstSel.currentRowChanged.connect(self.change_Stack)

        pixmap = QPixmap('../../../images/Lighthouse.jpg')
        self.lblImage.setPixmap(pixmap)
        self.lblImage.resize(pixmap.size())

    def change_Stack(self, index):
        self.stackedWidget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
