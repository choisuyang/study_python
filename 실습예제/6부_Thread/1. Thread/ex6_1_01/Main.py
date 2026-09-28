import sys, os, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mythread import MyThread
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
        self.toggle = 0
		# Thread 생성 및 시그널 슬롯 연결
        
		self.btnStart.clicked.connect(self.start_click)
        self.btnStop.clicked.connect(self.stop_click)
        
    def handle_command(self, cmd):
		pass

    def start_click(self):
        pass

    def stop_click(self):
        pass 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec())
