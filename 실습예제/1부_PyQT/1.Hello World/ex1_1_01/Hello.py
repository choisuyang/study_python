import sys
from PyQt5.QtWidgets import *


if __name__ == '__main__':

    print(__name__)

    app = QApplication(sys.argv)

    w = QWidget()
    w.setGeometry(500,500,200,50)
    w.setWindowTitle('PyQT')

    label = QLabel(w)
    label.setText("Hello Worlddasf")
    label.move(100,20)
    w.show()

    # sys.exit(app.exec_())
    app.exec()


