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
        self.btnAdd.clicked.connect(self.addMultiItem)
        self.btnRemove.clicked.connect(self.removeSingleItem)
        self.btnUp.clicked.connect(lambda: self.moveUpDown(-1))
        self.btnDown.clicked.connect(lambda: self.moveUpDown(1))
        self.addList()

        self.lstItemFrom.itemSelectionChanged.connect(self.fromDisplayInfo)
        self.lstItemTo.itemSelectionChanged.connect(self.toDisplayInfo)
        self.lstItemTo.currentTextChanged.connect(self.displayText)

    def moveUpDown(self, dir):
        r = self.lstItemTo.currentRow()
        item = self.lstItemTo.takeItem(r)
        self.lstItemTo.insertItem(r - dir, item)
        self.lstItemTo.setCurrentItem(item)


    def fromDisplayInfo(self):
        sel_cnt = len(self.lstItemFrom.selectedItems())
        self.lblFromSel.setText('선택된 item수: %d' % sel_cnt)

    def toDisplayInfo(self):
        sel_cnt = len(self.lstItemTo.selectedItems())
        self.lblToSel.setText('선택된 item수: %d' % sel_cnt)

    def displayText(self, text):
        self.lblToText.setText('선택된 item: %s' % text)

    def addList(self):
        l = ['additem:%d' % x for x in range(1, 20)]
        # self.lstItemFrom.addItems(l)

        for item in l:
            new_item = QListWidgetItem()
            new_item.setText(item)
            self.lstItemFrom.addItem(new_item)

    def addMultiItem(self):
        src = self.lstItemFrom
        dest = self.lstItemTo
        if src.selectedItems():
            for item in src.selectedItems():
                row_num = src.row(item)
                r = src.takeItem(row_num)
                dest.addItem(r)

    def removeSingleItem(self):
        src = self.lstItemTo
        dest = self.lstItemFrom
        if src.currentItem():
            row = src.currentRow()
            dest.addItem(src.takeItem(row))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
