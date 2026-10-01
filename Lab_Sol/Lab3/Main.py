import sys, subprocess
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

# def getSaveFile(self):
#         show_filter = "모든 파일(*.*);;텍스트파일(*.txt);; 파이썬파일(*.py)"
#         init_filter = "파이썬파일(*.py)"

#         opt = QFileDialog.Option()
#         # opt = QFileDialog.DontConfirmOverwrite

#         filepath, filter_type = QFileDialog.getSaveFileName(filter=show_filter, initialFilter=init_filter, options=opt)
#         print(filepath, filter_type)
#         if filepath:
#             self.lblSaveFileName.setText(filepath.split('/')[-1])
#             self.setWindowTitle(QFileInfo(filepath).fileName())



class Form(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnOpen.clicked.connect(self.openFile)


    def openFile(self):    
        show_filter = "비트맵 파일(*.bmp);;JPEG(*.jpg;*.jpeg);;GIF(*.gif);;PNG(*.png);;ICO(*.ICO)"
        init_filter = "비트맵 파일(*.bmp)"

        opt = QFileDialog.Option()

        filepath, filter_type = QFileDialog.getOpenFileName(filter=show_filter, initialFilter=init_filter, options=opt)
        if not filepath: return

        pixmap = QPixmap(filepath)
        self.lblImage.setPixmap(pixmap)
        self.lblImage.resize(pixmap.size())
        self.setWindowTitle("이미지뷰어 : " + QFileInfo(filepath).fileName())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
