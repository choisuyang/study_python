import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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

        self.btngetOpenFile.clicked.connect(self.getOpenFile)
        self.btngetSaveFile.clicked.connect(self.getSaveFile)
        self.btnExitDir.clicked.connect(self.getExistDir)
        self.btnExitDirUrl.clicked.connect(self.getExistDirUrl)

    def getOpenFile(self):
        show_filter = "모든 파일(*.*);;텍스트파일(*.txt);; 파이썬파일(*.py)"
        init_filter = "파이썬파일(*.py)"
        filepath, filter_type = QFileDialog.getOpenFileName(filter=show_filter, initialFilter=init_filter)
        print(filepath, filter_type)

        if filepath:
            self.lblOpenFileName.setText(filepath.split('/')[-1])
            self.setWindowTitle(QFileInfo(filepath).fileName())

    def getSaveFile(self):
        show_filter = "모든 파일(*.*);;텍스트파일(*.txt);; 파이썬파일(*.py)"
        init_filter = "파이썬파일(*.py)"

        opt = QFileDialog.Option()
        # opt = QFileDialog.DontConfirmOverwrite

        filepath, filter_type = QFileDialog.getSaveFileName(filter=show_filter, initialFilter=init_filter, options=opt)
        print(filepath, filter_type)
        if filepath:
            self.lblSaveFileName.setText(filepath.split('/')[-1])
            self.setWindowTitle(QFileInfo(filepath).fileName())

    def getExistDir(self):
        r = QFileDialog.getExistingDirectory(directory=self.linePath.text())
        self.linePath.setText(r)

    def getExistDirUrl(self):
        r = QFileDialog.getExistingDirectoryUrl(directory=QUrl(self.linePath.text()))
        print(r.toString())
        self.linePathUrl.setText(r.toString())
        url_link = '<a href="' + r.toString() + '">' + r.toString() + '</a>'
        self.label.setText(url_link)
        self.label.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
