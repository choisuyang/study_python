import os
import random
import sys
from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QColor

# 선택지: 이름 -> 이모지
CHOICES = {"가위": "✌️", "바위": "✊", "보": "✋"}
# key 가 value 를 이긴다
BEATS = {"가위": "보", "바위": "가위", "보": "바위"}

RESULT_STYLE = {
    "승리": ("🎉 승리!", "#2e9e4f"),
    "패배": ("😢 패배...", "#d9534f"),
    "무승부": ("🤝 무승부", "#888888"),
}


class RPSWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui.ui")
        uic.loadUi(ui_path, self)

        self.wins = 0
        self.losses = 0
        self.draws = 0

        self.btnScissors.clicked.connect(lambda: self.play("가위"))
        self.btnRock.clicked.connect(lambda: self.play("바위"))
        self.btnPaper.clicked.connect(lambda: self.play("보"))
        self.btnReset.clicked.connect(self.reset)

        self.update_stats()

    # ---------- 게임 로직 ----------
    @staticmethod
    def judge(player, computer):
        if player == computer:
            return "무승부"
        return "승리" if BEATS[player] == computer else "패배"

    def play(self, player):
        computer = random.choice(list(CHOICES))  # 컴퓨터는 랜덤 선택
        result = self.judge(player, computer)

        if result == "승리":
            self.wins += 1
        elif result == "패배":
            self.losses += 1
        else:
            self.draws += 1

        # 화면 갱신
        self.lblPlayer.setText(CHOICES[player])
        self.lblComputer.setText(CHOICES[computer])
        text, color = RESULT_STYLE[result]
        self.lblResult.setText(text)
        self.lblResult.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {color};")

        self.add_history(player, computer, result)
        self.update_stats()

    # ---------- 히스토리 ----------
    def add_history(self, player, computer, result):
        now = datetime.now().strftime("%H:%M:%S")
        n = self.wins + self.losses + self.draws
        text = (f"#{n}  [{now}]  나 {CHOICES[player]}{player}  vs  "
                f"{CHOICES[computer]}{computer} 컴퓨터  →  {result}")
        item = QtWidgets.QListWidgetItem(text)
        item.setForeground(QColor(RESULT_STYLE[result][1]))
        self.listHistory.insertItem(0, item)  # 최신 기록이 맨 위

    # ---------- 통계 ----------
    def update_stats(self):
        total = self.wins + self.losses + self.draws
        rate = (self.wins / total * 100) if total else 0.0

        # 대시보드 탭
        self.lblTotal.setText(str(total))
        self.lblWins.setText(str(self.wins))
        self.lblLosses.setText(str(self.losses))
        self.lblDraws.setText(str(self.draws))
        self.lblDashRate.setText(f"승률 {rate:.1f}%")
        self.progressDash.setValue(round(rate))

        # 대결 탭
        self.lblWinRate.setText(
            f"승률 {rate:.1f}% ({self.wins}승 {self.losses}패 {self.draws}무)"
        )
        self.progressWinRate.setValue(round(rate))

    def reset(self):
        self.wins = self.losses = self.draws = 0
        self.listHistory.clear()
        self.lblPlayer.setText("❔")
        self.lblComputer.setText("❔")
        self.lblResult.setText("결과가 여기에 표시됩니다")
        self.lblResult.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.update_stats()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RPSWindow()
    window.show()
    sys.exit(app.exec_())
