from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import *


class myEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Insert:
            self.setOverwriteMode(not self.overwriteMode())
        QPlainTextEdit.keyPressEvent(self, event)

