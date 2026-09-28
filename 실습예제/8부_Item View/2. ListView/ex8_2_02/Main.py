import sys, subprocess, json
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


class MyModel(QAbstractListModel):
    def __init__(self, strlist=None):
        super().__init__()
        self.strlist = strlist or []

    def rowCount(self, parent=None):
        return len(self.strlist)

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.strlist[index.row()]
        return QVariant()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index, any, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False
        self.strlist[index.row()] = any
        self.dataChanged.emit(index, index)
        return True

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return 'column %d' % section
        else:
            return 'row %d' % section

    def insertRow(self, pos):
        self.beginInsertRows(QModelIndex(), pos, pos)
        self.strlist.insert(pos, '')
        self.endInsertRows()
        return True

    def removeRow(self, pos):
        self.beginRemoveRows(QModelIndex(), pos, pos)
        del self.strlist[pos]
        self.endRemoveRows()
        return True


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.model = MyModel(self.loadFile())
        self.listView.setModel(self.model)
        self.tableView.setModel(self.model)

        self.btnAdd.clicked.connect(self.addData)
        self.btnInsert.clicked.connect(self.insertData)
        self.btnDelete.clicked.connect(self.deleteData)
        self.model.dataChanged.connect(self.dataChange)

    def dataChange(self, index):
        print('data changed:', index.data())

    def addRow(self, index):
        if self.lineEdit.text():
            self.model.setData(index, self.lineEdit.text())
        else:
            self.listView.edit(index)
        self.listView.setCurrentIndex(index)

    def focusRow(self, row, edit_disable):
        index = self.model.index(row)
        if not edit_disable:
            self.listView.edit(index)
        self.listView.setCurrentIndex(index)

    def addData(self):
        # [예제1] 코드
        # row = self.model.rowCount(QModelIndex())
        # self.model.insertRow(row)
        # index = self.model.index(row)
        # self.addRow(index)

        self.model.layoutAboutToBeChanged.emit()
        self.model.strlist.append(self.lineEdit.text())
        row = len(self.model.strlist) - 1
        index = self.model.index(row)
        self.model.changePersistentIndex(index, index)
        self.model.layoutChanged.emit()
        self.focusRow(row, self.lineEdit.text())
        self.saveFile()

    def insertData(self):
        # #[예제1] 코드
        # row = self.listView.currentIndex().row()
        # self.model.insertRow(row)
        # index = self.model.index(row)
        # self.addRow(index)

        row = self.listView.currentIndex().row()
        self.model.strlist.insert(row, self.lineEdit.text())
        self.model.layoutChanged.emit()

        self.focusRow(row, self.lineEdit.text())
        self.saveFile()

    def deleteData(self):
        # #[예제1] 코드
        # self.model.removeRow(self.listView.currentIndex().row())

        del self.model.strlist[self.listView.currentIndex().row()]
        self.model.layoutChanged.emit()
        self.saveFile()

    def loadFile(self):
        l = []
        try:
            with open('list.json', 'r') as f:
                l = json.load(f)
            return l
        except Exception as e:
            print(type(e).__name__, e)

    def saveFile(self):
        with open('list.json', 'w') as f:
            json.dump(self.model.strlist, f)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
