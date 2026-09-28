from PyQt5.QtWidgets import QPushButton


class myButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.clickCount = 0

    def mousePressEvent(self, event):
        self.setStyleSheet("background-color: rgb(255, 0, 0);")
        QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet('background-color: rgb(0, 255, 0);')
        self.clickCount = self.clickCount + 1
        QPushButton.mouseReleaseEvent(self, event)

    def getCount(self):
        return self.clickCount
