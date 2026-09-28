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

        self.statusbar.addPermanentWidget(self.progressBar, 0)
        self.statusbar.addWidget(self.lblDate, 0)

        self.lblDate.setText(self.calendarWidget.selectedDate().toString('yyyy년 MM월 dd일'))
        self.calendarWidget.clicked.connect(self.dispDate)

    def dispDate(self, date):
        strdate = date.toString('yyyy년 MM월 dd일')
        self.statusbar.showMessage(strdate, 1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
