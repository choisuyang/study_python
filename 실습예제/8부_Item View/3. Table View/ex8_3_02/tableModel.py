from PyQt5.QtCore import *
from PyQt5.QtGui import QColor


class TableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self.contents = data or []

    def setModelData(self, lst):
        self.contents = lst

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.contents[index.row() + 1][index.column()]
        return QVariant()

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return self.contents[0][section]
        else:
            return section + 1

    def rowCount(self, index):
        return len(self.contents) - 1

    def columnCount(self, index):
        return len(self.contents[0])

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            self.contents[index.row() + 1][index.column()] = value
            self.dataChanged.emit(index, index)

            return True
        return False
