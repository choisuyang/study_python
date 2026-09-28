import sys, subprocess, glob
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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
        self.btnBack.clicked.connect(self.changeBackground)
        self.btnAddCheck.clicked.connect(self.addCheck)
        self.btnIcon.clicked.connect(self.addIcon)
        self.btnSnap.clicked.connect(self.setSnap)
        self.btnFree.clicked.connect(self.setFree)
        self.buttonGroup.buttonClicked.connect(self.globTest)

    def globTest(self, btn):
        # 파일명이 test로 끝나는 png파일
        if btn == self.btnTest:
            pattern =''

        # 2로 시작하고 old로 끝나는 png파일
        elif btn == self.btnOld:
            pattern =''

        # menu이미지 중 일련번호 두 번째 수가 1인 png
        elif btn==self.btnMenu:
            pattern =''

        # 숫자로 시작 하는 png
        elif btn==self.btnNum:
            pattern =''

        # 확장자가 png인 파일
        elif btn == self.btnPng:
            pattern =''

        # 확장자가 jpg인 파일
        elif btn == self.btnJpg:
            pattern =''

        # 모든 파일
        else:
            pattern = ''

        self.lstFrom.clear()
        l = glob.glob(pattern)
        for item in l:
            new_item = QListWidgetItem()
            new_item.setIcon(QIcon(item))
            new_item.setText(item.split('\\')[-1])
            self.lstFrom.addItem(new_item)

    def setSnap(self):
        self.lstTo.setMovement(QListView.Snap)

    def setFree(self):
        self.lstTo.setMovement(QListView.Free)

    def changeBackground(self):
        self.lstFrom.clear()
        for i in range(10):
            new_item = QListWidgetItem()
            new_item.setText('additem %d' % i)
            new_item.setBackground(Qt.yellow)
            new_item.setForeground(Qt.red)
            self.lstFrom.addItem(new_item)

    def addCheck(self):
        self.lstFrom.clear()
        for i in range(10):
            new_item = QListWidgetItem()
            new_item.setText('additem %d' % i)
            new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable)
            new_item.setCheckState(Qt.Unchecked)
            self.lstFrom.addItem(new_item)

    def addIcon(self):
        self.lstFrom.clear()
        it = QDirIterator('./images', QDirIterator.Subdirectories)

        while it.hasNext():
            new_item = QListWidgetItem()
            new_item.setIcon(QIcon(it.next()))
            new_item.setText(it.fileName())
            self.lstFrom.addItem(new_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
