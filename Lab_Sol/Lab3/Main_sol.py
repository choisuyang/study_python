import sys, subprocessos
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QFileInfo

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
        self.btnOpen.clicked.connect(self.openFile)

    def openFile(self):
        show_filter = "비트맵 파일(*.bmp);;JPEG (*.jpg; *.jpeg);;GIF (*.gif);; PNG (*.png);; ICO(*.ICO)"
        init_filter = 'JPEG (*.jpg; *.jpeg)'
        file_path, filter_type = QFileDialog.getOpenFileName(filter=show_filter, initialFilter=init_filter)
        if not file_path: return
        pixmap = QPixmap(file_path)
        self.lblImage.setPixmap(pixmap)
        self.lblImage.resize(pixmap.size())
        self.setWindowTitle("이미지뷰어 : " + QFileInfo(file_path).fileName())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
