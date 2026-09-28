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
    ins_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.txtEditor.installEventFilter(self)
        self.pushButton.installEventFilter(self)
        self.ins_signal.connect(self.chageIns)

        self.pushButton.clicked.connect(self.func)

    def eventFilter(self, obj, event):
        if obj == self.pushButton:
            if event.type() == QEvent.MouseButtonPress or \
                    event.type() == QEvent.MouseButtonRelease:
                return True
        if obj == self.txtEditor:
            if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Insert:
                # self.ins_signal.emit(self.txtEditor.overwriteMode())
                self.chageIns(self.txtEditor.overwriteMode())
        return False

    def chageIns(self, state):
        self.txtEditor.setOverwriteMode(not state)
        print('Key Event')

    def func(self):
        self.label.setText('button click')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    # app.installEventFilter(w)
    w.show()
    sys.exit(app.exec_())
