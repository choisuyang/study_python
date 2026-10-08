import json
import os
import random
import sys
from datetime import datetime
import shutil

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import (QBrush, QColor, QFont, QImage, QLinearGradient,
                         QPainter, QPixmap)

try:
    import cv2  # 웹캠 촬영용 (없으면 기념 카드로 대체)
except ImportError:
    cv2 = None

# ---------------- 설정값 ----------------
MIN_RATE = 25.0        # 기념사진 최소 승률(%)
MIN_GAMES = 5          # 승률 집계 최소 대결 수 (1판 1승=100% 방지, 1로 바꾸면 비활성)
COUNTDOWN_START = 5    # 카운트다운 시작 숫자
MAX_RANK = 10          # 랭킹 최대 인원

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO_DIR = os.path.join(BASE_DIR, "photos")
RANK_FILE = os.path.join(BASE_DIR, "ranking.json")

# 선택지: 이름 -> 이모지
CHOICES = {"가위": "✌️", "바위": "✊", "보": "✋"}
# key 가 value 를 이긴다
BEATS = {"가위": "보", "바위": "가위", "보": "바위"}

RESULT_STYLE = {
    "승리": ("🎉 승리!", "#2e9e4f"),
    "패배": ("😢 패배...", "#d9534f"),
    "무승부": ("🤝 무승부", "#888888"),
}
MEDALS = ["🥇", "🥈", "🥉"]


class RPSWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(BASE_DIR, "gui.ui"), self)

        self.wins = self.losses = self.draws = 0
        self.ranking = self.load_ranking()

        # 촬영 관련 상태
        self.cap = None
        self.last_image = None
        self.photo_ctx = None
        self.count = 0
        self.count_timer = QTimer(self)
        self.count_timer.timeout.connect(self.on_count_tick)
        self.preview_timer = QTimer(self)
        self.preview_timer.timeout.connect(self.update_preview)

        # 버튼 연결
        self.btnScissors.clicked.connect(lambda: self.play("가위"))
        self.btnRock.clicked.connect(lambda: self.play("바위"))
        self.btnPaper.clicked.connect(lambda: self.play("보"))
        self.btnReset.clicked.connect(self.reset)
        self.btnRankReset.clicked.connect(self.reset_ranking)

        self.setup_rank_table()
        self.update_stats()
        self.refresh_ranking()

    # =============== 게임 로직 ===============
    @staticmethod
    def judge(player, computer):
        if player == computer:
            return "무승부"
        return "승리" if BEATS[player] == computer else "패배"

    def total_games(self):
        return self.wins + self.losses + self.draws

    def win_rate(self):
        total = self.total_games()
        return (self.wins / total * 100) if total else 0.0

    def current_name(self):
        return self.leName.text().strip() or "플레이어"

    def play(self, player):
        if not self.btnRock.isEnabled():
            return
        self.leName.setEnabled(False)  # 대결 시작 후에는 이름 고정(초기화 시 해제)
        computer = random.choice(list(CHOICES))  # 컴퓨터는 랜덤 선택
        result = self.judge(player, computer)

        if result == "승리":
            self.wins += 1
        elif result == "패배":
            self.losses += 1
        else:
            self.draws += 1

        self.lblPlayer.setText(CHOICES[player])
        self.lblComputer.setText(CHOICES[computer])
        text, color = RESULT_STYLE[result]
        self.lblResult.setText(text)
        self.lblResult.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {color};")

        self.add_history(player, computer, result)
        self.update_stats()

        if self.total_games() >= MIN_GAMES:
            self.check_record(self.current_name(), self.win_rate())

    def add_history(self, player, computer, result):
        now = datetime.now().strftime("%H:%M:%S")
        text = (f"#{self.total_games()}  [{now}]  나 {CHOICES[player]}{player}  vs  "
                f"{CHOICES[computer]}{computer} 컴퓨터  →  {result}")
        item = QtWidgets.QListWidgetItem(text)
        item.setForeground(QColor(RESULT_STYLE[result][1]))
        self.listHistory.insertItem(0, item)  # 최신 기록이 맨 위

    def update_stats(self):
        total = self.total_games()
        rate = self.win_rate()

        self.lblTotal.setText(str(total))
        self.lblWins.setText(str(self.wins))
        self.lblLosses.setText(str(self.losses))
        self.lblDraws.setText(str(self.draws))
        self.lblDashRate.setText(f"승률 {rate:.1f}%")
        self.progressDash.setValue(round(rate))

        self.lblWinRate.setText(
            f"승률 {rate:.1f}% ({self.wins}승 {self.losses}패 {self.draws}무)")
        self.progressWinRate.setValue(round(rate))

    def reset(self):
        self.wins = self.losses = self.draws = 0
        self.listHistory.clear()
        self.lblPlayer.setText("❔")
        self.lblComputer.setText("❔")
        self.lblResult.setText("결과가 여기에 표시됩니다")
        self.lblResult.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.leName.setEnabled(True)
        self.update_stats()

    def set_game_enabled(self, enabled):
        for w in (self.btnScissors, self.btnRock, self.btnPaper, self.btnReset):
            w.setEnabled(enabled)

    # =============== 랭킹 데이터 ===============
    @staticmethod
    def load_ranking():
        try:
            with open(RANK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def save_ranking(self):
        with open(RANK_FILE, "w", encoding="utf-8") as f:
            json.dump(self.ranking, f, ensure_ascii=False, indent=2)

    def sorted_ranking(self):
        items = sorted(self.ranking.items(),
                       key=lambda kv: (kv[1]["best_rate"], kv[1]["total"]),
                       reverse=True)
        return items[:MAX_RANK]

    def top_rate(self):
        items = self.sorted_ranking()
        return items[0][1]["best_rate"] if items else 0.0
    def check_record(self, name, rate):
        """플레이어별: 승률 30%↑ 이고 본인 최고 승률을 넘으면 랭킹 등록 + 기념사진"""
        if rate < MIN_RATE:
            return

        entry = self.ranking.get(name)
        if entry is not None and rate <= entry["best_rate"]:
            return  # 본인 최고 승률을 넘지 못함

        # 1) 알림창이 뜨기 전에 버튼부터 잠금 (연타 방지)
        self.set_game_enabled(False)

        self.ranking[name] = {
            "best_rate": rate,
            "wins": self.wins,
            "total": self.total_games(),
            "photo": entry["photo"] if entry else None,
        }
        self.save_ranking()
        self.refresh_ranking()

        # 2) 알림창 (확인을 눌러야 다음으로 진행)
        QtWidgets.QMessageBox.information(
            self, "기념촬영",
            f"🎉 {name}님, 승률 {rate:.1f}% 달성!\n\n"
            "기념촬영을 시작하겠습니다.\n"
            "확인을 누르면 카운트다운이 시작됩니다.")

        # 3) 확인 후 촬영 시작 (탭 이동 + 카운트다운)
        self.start_photo_sequence(name, rate)

    # =============== 기념사진 ===============
    def start_photo_sequence(self, name, rate):
        self.photo_ctx = (name, rate)
        self.last_image = None
        self.set_game_enabled(False)
        self.tabWidget.setCurrentWidget(self.tabPhoto)
        self.lblPhotoTitle.setText(
            f"🎉 {name}님 승률 {rate:.1f}% - 1위 기록 경신! 카메라를 봐주세요")
        self.lblPhotoInfo.setText("")
        self.open_camera()

        self.count = COUNTDOWN_START
        self.lblCountdown.setText(str(self.count))
        self.count_timer.start(1000)
        self.preview_timer.start(33)

    def on_count_tick(self):
        self.count -= 1
        if self.count > 0:
            self.lblCountdown.setText(str(self.count))
        else:  # 1이 표시되고 1초 뒤 촬영
            self.count_timer.stop()
            self.take_photo()

    def open_camera(self):
        self.cap = None
        if cv2 is None:
            self.lblCamera.setText("opencv-python 미설치 → 기념 카드로 대체됩니다")
            return
        cap = (cv2.VideoCapture(0, cv2.CAP_DSHOW) if sys.platform == "win32"
               else cv2.VideoCapture(0))
        if cap.isOpened():
            self.cap = cap
        else:
            cap.release()
            self.lblCamera.setText("카메라를 찾을 수 없음 → 기념 카드로 대체됩니다")

    def close_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def read_frame(self):
        if self.cap is None:
            return None
        ok, frame = self.cap.read()
        if not ok:
            return None
        frame = cv2.flip(frame, 1)  # 거울 모드
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        return QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888).copy()

    def update_preview(self):
        image = self.read_frame()
        if image is not None:
            self.last_image = image
            self.show_image(image)

    def show_image(self, image):
        pix = QPixmap.fromImage(image).scaled(
            self.lblCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lblCamera.setPixmap(pix)

    def take_photo(self):
        self.preview_timer.stop()
        name, rate = self.photo_ctx
        self.lblCountdown.setText("📸")

        image = self.read_frame()
        if image is None:
            image = self.last_image
        if image is None:
            image = self.make_fallback_image()
        self.close_camera()

        image = self.decorate(image, name, rate)
        os.makedirs(PHOTO_DIR, exist_ok=True)
        filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image.save(os.path.join(PHOTO_DIR, filename))

        self.ranking[name]["photo"] = f"photos/{filename}"
        self.save_ranking()
        self.refresh_ranking()

        self.show_image(image)
        self.lblPhotoInfo.setText(
            f"✅ 기념사진 저장 완료: photos/{filename}  (랭킹 탭에서 확인하세요)")
        self.set_game_enabled(True)

    @staticmethod
    def make_fallback_image():
        img = QImage(640, 480, QImage.Format_RGB32)
        p = QPainter(img)
        grad = QLinearGradient(0, 0, 640, 480)
        grad.setColorAt(0, QColor("#f6d365"))
        grad.setColorAt(1, QColor("#fda085"))
        p.fillRect(img.rect(), QBrush(grad))
        p.setPen(Qt.white)
        font = QFont()
        font.setPixelSize(40)
        font.setBold(True)
        p.setFont(font)
        p.drawText(img.rect(), Qt.AlignCenter, "WINNER!")
        p.end()
        return img

    @staticmethod
    def decorate(image, name, rate):
        img = image.convertToFormat(QImage.Format_RGB32)
        w, h = img.width(), img.height()
        p = QPainter(img)
        p.fillRect(0, h - 80, w, 80, QColor(0, 0, 0, 150))
        p.setPen(Qt.white)
        font = QFont()
        font.setPixelSize(30)
        font.setBold(True)
        p.setFont(font)
        p.drawText(20, h - 80, w - 40, 50, Qt.AlignVCenter | Qt.AlignLeft,
                   f"{name}  승률 {rate:.1f}%")
        font.setPixelSize(16)
        font.setBold(False)
        p.setFont(font)
        p.drawText(20, h - 35, w - 40, 25, Qt.AlignVCenter | Qt.AlignLeft,
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        p.end()
        return img

    # =============== 랭킹 탭 UI ===============
    def setup_rank_table(self):
        t = self.tableRank
        t.setColumnCount(5)
        t.setRowCount(MAX_RANK)
        t.setHorizontalHeaderLabels(["순위", "이름", "최고 승률", "전적", "기념사진"])
        t.verticalHeader().setVisible(False)
        t.verticalHeader().setDefaultSectionSize(84)
        t.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        t.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        header = t.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        t.setColumnWidth(4, 130)
        t.cellClicked.connect(self.on_rank_cell_clicked)

    def refresh_ranking(self):
        t = self.tableRank
        items = self.sorted_ranking()
        t.clearContents()

        for row in range(MAX_RANK):
            t.removeCellWidget(row, 4)
            if row >= len(items):
                continue
            name, e = items[row]
            rank_text = MEDALS[row] if row < 3 else str(row + 1)
            cells = [rank_text, name, f"{e['best_rate']:.1f}%",
                     f"{e['wins']}승 / {e['total']}판"]
            for col, text in enumerate(cells):
                item = QtWidgets.QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                t.setItem(row, col, item)

            photo_item = QtWidgets.QTableWidgetItem("")
            photo_path = e.get("photo")
            full = os.path.join(BASE_DIR, photo_path) if photo_path else None
            if full and os.path.exists(full):
                photo_item.setData(Qt.UserRole, full)
                label = QtWidgets.QLabel()
                label.setAlignment(Qt.AlignCenter)
                label.setAttribute(Qt.WA_TransparentForMouseEvents)
                label.setPixmap(QPixmap(full).scaled(
                    110, 78, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                t.setCellWidget(row, 4, label)
            else:
                photo_item.setText("사진 없음")
                photo_item.setTextAlignment(Qt.AlignCenter)
            t.setItem(row, 4, photo_item)

        self.update_top_label(items)

    def update_top_label(self, items):
        cond = (f"기념사진 조건: 승률 {MIN_RATE:.0f}% 이상 + 본인 최고 승률 경신 (최소 {MIN_GAMES}판)")
        # cond = (f"기념사진 조건: 승률 {MIN_RATE:.0f}% 이상 + 1위 초과 (최소 {MIN_GAMES}판)")
        if items:
            name, e = items[0]
            self.lblTopRate.setText(
                f"🏆 현재 1위: {name} {e['best_rate']:.1f}%\n{cond}")
        else:
            self.lblTopRate.setText(f"현재 1위 기록 없음\n{cond}")

    def on_rank_cell_clicked(self, row, col):
        if col != 4:
            return
        item = self.tableRank.item(row, 4)
        path = item.data(Qt.UserRole) if item else None
        if not path or not os.path.exists(path):
            return
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("기념사진")
        lay = QtWidgets.QVBoxLayout(dlg)
        lbl = QtWidgets.QLabel()
        lbl.setPixmap(QPixmap(path).scaled(
            720, 540, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        lay.addWidget(lbl)
        dlg.exec_()

    def reset_ranking(self):
        if self.count_timer.isActive():  # 촬영 카운트다운 중에는 무시
            return

        answer = QtWidgets.QMessageBox.question(
            self, "랭킹 초기화",
            "랭킹 기록과 저장된 기념사진이 모두 삭제됩니다.\n계속할까요?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if answer != QtWidgets.QMessageBox.Yes:
            return

        self.ranking = {}
        self.save_ranking()                              # ranking.json 비우기
        shutil.rmtree(PHOTO_DIR, ignore_errors=True)     # photos/ 폴더 삭제

        # 기념사진 탭 화면도 초기 상태로
        self.lblCamera.clear()
        self.lblCamera.setText("아직 촬영 전입니다")
        self.lblCountdown.setText("-")
        self.lblPhotoInfo.setText("")

        self.refresh_ranking()                           # 테이블과 1위 표시 갱신
    

    def closeEvent(self, event):
        self.close_camera()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RPSWindow()
    window.show()
    sys.exit(app.exec_())
