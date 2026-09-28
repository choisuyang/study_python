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
        self.btnGroupDisp.buttonClicked.connect(self.dispNum)
        self.btnGroupOp.buttonClicked.connect(self.operate)
        self.expr = ''

    def dispNum(self, btn):
        self.expr = self.expr + btn.text()
        self.lblDisp.setText(self.expr)

    def operate(self, btn):

        if btn == self.btnBack:
            self.expr = self.expr[0:-1]
            self.lblDisp.setText(self.expr) if self.expr else self.lblDisp.setText('0')
        elif btn == self.btnC:
            self.expr = ''
            self.lblDisp.setText('0')
        elif btn == self.btnResult:
            try:
                self.lblDisp.setText(str(eval(self.expr)))
            except ZeroDivisionError:
                self.lblDisp.setText("0으로 나눌 수 없습니다")
            except SyntaxError:
                self.lblDisp.setText("잘못된 수식 입니다")
            except Exception as e:
                self.lblDisp.setText("오류")
            self.expr = ''
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
