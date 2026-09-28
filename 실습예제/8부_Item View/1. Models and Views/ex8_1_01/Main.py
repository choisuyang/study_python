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
        self.model = None
        self.setupUi(self)

        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath('')
        self.treeView.setModel(self.dir_model)
        self.treeView.clicked.connect(self.treeView_clicked)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath('')
        self.listView.setModel(self.file_model)
        self.listView.clicked.connect(self.listView_clicked)

    def treeView_clicked(self, index):
        path = self.dir_model.fileInfo(index).absoluteFilePath()
        self.listView.setRootIndex(self.file_model.setRootPath(path))

    def listView_clicked(self, index):
        print(self.file_model.filePath(index))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
