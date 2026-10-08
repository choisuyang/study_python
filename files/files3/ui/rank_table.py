"""랭킹 탭의 표(QTableWidget) 설정 / 갱신 / 사진 확대 팝업 전담 클래스."""
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from config import BASE_DIR, MAX_RANK, MEDALS


class RankTable:
    def __init__(self, table, parent):
        """table: gui.ui 의 tableRank / parent: 팝업창의 부모(메인 윈도우)"""
        self.table = table
        self.parent = parent
        self._setup()

    def _setup(self):
        """열 구성과 표 모양을 한 번만 설정한다."""
        t = self.table
        t.setColumnCount(5)
        t.setRowCount(MAX_RANK)
        t.setHorizontalHeaderLabels(["순위", "이름", "최고 승률", "전적", "기념사진"])
        t.verticalHeader().setVisible(False)
        t.verticalHeader().setDefaultSectionSize(84)   # 사진이 보이도록 행 높이 확보
        t.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        t.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        header = t.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)  # 사진 열은 고정 폭
        t.setColumnWidth(4, 130)

        t.cellClicked.connect(self._on_cell_clicked)

    def refresh(self, items):
        """items = [(이름, 기록), ...] (이미 승률 순으로 정렬된 상태)로 표를 다시 그린다."""
        t = self.table
        t.clearContents()

        for row in range(MAX_RANK):
            t.removeCellWidget(row, 4)      # 이전에 넣은 사진 위젯 제거
            if row >= len(items):
                continue                    # 남는 줄은 빈칸

            name, e = items[row]
            rank_text = MEDALS[row] if row < 3 else str(row + 1)
            cells = [rank_text, name, f"{e['best_rate']:.1f}%",
                     f"{e['wins']}승 / {e['total']}판"]
            for col, text in enumerate(cells):
                item = QtWidgets.QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                t.setItem(row, col, item)

            self._set_photo_cell(row, e.get("photo"))

    def _set_photo_cell(self, row, rel_path):
        """사진 열: 파일이 있으면 썸네일, 없으면 '사진 없음' 글자"""
        item = QtWidgets.QTableWidgetItem("")
        full = os.path.join(BASE_DIR, rel_path) if rel_path else None

        if full and os.path.exists(full):
            item.setData(Qt.UserRole, full)   # 클릭 시 꺼내 쓰도록 전체 경로를 셀에 보관
            label = QtWidgets.QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setAttribute(Qt.WA_TransparentForMouseEvents)  # 클릭이 표까지 전달되게
            label.setPixmap(QPixmap(full).scaled(
                110, 78, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.table.setCellWidget(row, 4, label)
        else:
            item.setText("사진 없음")
            item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 4, item)

    def _on_cell_clicked(self, row, col):
        """사진 열을 클릭하면 큰 사진을 팝업으로 보여준다."""
        if col != 4:
            return
        item = self.table.item(row, 4)
        path = item.data(Qt.UserRole) if item else None
        if not path or not os.path.exists(path):
            return

        dlg = QtWidgets.QDialog(self.parent)
        dlg.setWindowTitle("기념사진")
        lay = QtWidgets.QVBoxLayout(dlg)
        lbl = QtWidgets.QLabel()
        lbl.setPixmap(QPixmap(path).scaled(
            720, 540, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        lay.addWidget(lbl)
        dlg.exec_()
