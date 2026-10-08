"""가위바위보 게임 - 진입점 / 메인 윈도우.

이 파일은 '화면(gui.ui)과 각 모듈을 연결하고 흐름을 제어'하는 역할만 합니다.

    config.py                 설정값, 경로, 표시용 상수
    core/game.py              가위바위보 규칙, 전적(승/패/무, 승률) 계산
    storage/ranking_store.py  ranking.json 저장/조회/삭제
    camera/camera_service.py  웹캠 열기/프레임 읽기
    camera/photo_utils.py     기념사진 꾸미기/저장
    ui/rank_table.py          랭킹 탭 표 UI
"""
import sys
from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPixmap

import config
from camera import photo_utils
from camera.camera_service import CameraService
from core.game import CHOICES, GameStats, judge, random_choice
from storage.ranking_store import RankingStore
from ui.rank_table import RankTable


class RPSWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.UI_FILE, self)   # gui.ui 의 위젯들이 self.위젯이름 으로 생성됨

        # ---- 각 기능 담당 객체 ----
        self.stats = GameStats()                       # 현재 플레이어의 승/패/무
        self.store = RankingStore()                    # 랭킹 데이터 (ranking.json)
        self.camera = CameraService()                  # 웹캠
        self.rank_table = RankTable(self.tableRank, self)  # 랭킹 탭 표

        # ---- 촬영 진행 상태 ----
        self.photo_ctx = None      # (이름, 승률) - 촬영 대상 정보
        self.last_image = None     # 마지막으로 성공한 미리보기 프레임
        self.count = 0             # 남은 카운트다운 숫자
        self.count_timer = QTimer(self)     # 1초마다: 숫자 줄이기
        self.count_timer.timeout.connect(self.on_count_tick)
        self.preview_timer = QTimer(self)   # 약 30fps: 카메라 미리보기 갱신
        self.preview_timer.timeout.connect(self.update_preview)

        # ---- 버튼 연결 ----
        self.btnScissors.clicked.connect(lambda: self.play("가위"))
        self.btnRock.clicked.connect(lambda: self.play("바위"))
        self.btnPaper.clicked.connect(lambda: self.play("보"))
        self.btnReset.clicked.connect(self.reset)
        self.btnRankReset.clicked.connect(self.reset_ranking)

        # ---- 첫 화면 그리기 ----
        self.update_stats()
        self.refresh_ranking()

    # =====================================================
    # 대결
    # =====================================================
    def current_name(self):
        """입력한 플레이어 이름 (비어 있으면 '플레이어')"""
        return self.leName.text().strip() or "플레이어"

    def play(self, player):
        """가위/바위/보 버튼을 눌렀을 때 한 판 진행"""
        if not self.btnRock.isEnabled():   # 촬영 준비 중(버튼 잠김)에는 무시
            return
        self.leName.setEnabled(False)      # 대결을 시작하면 이름 고정 (초기화 시 해제)

        computer = random_choice()         # 컴퓨터는 랜덤
        result = judge(player, computer)
        self.stats.add(result)

        # 결과 화면 갱신
        self.lblPlayer.setText(CHOICES[player])
        self.lblComputer.setText(CHOICES[computer])
        text, color = config.RESULT_STYLE[result]
        self.lblResult.setText(text)
        self.lblResult.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {color};")

        self.add_history(player, computer, result)
        self.update_stats()

        # 최소 대결 수를 채웠다면 기록 경신/촬영 여부 판정
        if self.stats.total >= config.MIN_GAMES:
            self.check_record(self.current_name(), self.stats.win_rate)

    def add_history(self, player, computer, result):
        """오른쪽 히스토리 목록 맨 위에 한 줄 추가"""
        now = datetime.now().strftime("%H:%M:%S")
        text = (f"#{self.stats.total}  [{now}]  나 {CHOICES[player]}{player}  vs  "
                f"{CHOICES[computer]}{computer} 컴퓨터  →  {result}")
        item = QtWidgets.QListWidgetItem(text)
        item.setForeground(QColor(config.RESULT_STYLE[result][1]))
        self.listHistory.insertItem(0, item)   # 최신 기록이 맨 위

    def update_stats(self):
        """대시보드 탭과 대결 탭의 숫자/승률 바를 현재 전적으로 갱신"""
        s = self.stats
        rate = s.win_rate

        # 대시보드 탭
        self.lblTotal.setText(str(s.total))
        self.lblWins.setText(str(s.wins))
        self.lblLosses.setText(str(s.losses))
        self.lblDraws.setText(str(s.draws))
        self.lblDashRate.setText(f"승률 {rate:.1f}%")
        self.progressDash.setValue(round(rate))

        # 대결 탭
        self.lblWinRate.setText(f"승률 {rate:.1f}% ({s.wins}승 {s.losses}패 {s.draws}무)")
        self.progressWinRate.setValue(round(rate))

    def reset(self):
        """'기록 초기화' 버튼: 현재 플레이어의 전적/히스토리만 초기화 (랭킹은 유지)"""
        self.stats.reset()
        self.listHistory.clear()
        self.lblPlayer.setText("❔")
        self.lblComputer.setText("❔")
        self.lblResult.setText("결과가 여기에 표시됩니다")
        self.lblResult.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.leName.setEnabled(True)   # 새 플레이어로 이름 변경 가능
        self.update_stats()

    def set_game_enabled(self, enabled):
        """대결 버튼 3개 + 초기화 버튼을 한꺼번에 켜고 끈다 (촬영 중 연타 방지)"""
        for w in (self.btnScissors, self.btnRock, self.btnPaper, self.btnReset):
            w.setEnabled(enabled)

    # =====================================================
    # 기록 경신 판정
    # =====================================================
    def check_record(self, name, rate):
        """플레이어별: 승률이 MIN_RATE 이상이고 '본인 최고 승률'을 넘으면 랭킹 등록 + 기념사진"""
        if rate < config.MIN_RATE:
            return

        entry = self.store.get(name)
        if entry is not None and rate <= entry["best_rate"]:
            return   # 본인 최고 승률을 넘지 못함

        # 1) 알림창이 뜨기 전에 버튼부터 잠금 (연타 방지)
        self.set_game_enabled(False)

        # 2) 랭킹에 먼저 등록 (사진은 촬영 후 연결)
        self.store.update_best(name, rate, self.stats.wins, self.stats.total)
        self.refresh_ranking()

        # 3) 알림창 - 확인을 눌러야 다음으로 진행
        QtWidgets.QMessageBox.information(
            self, "기념촬영",
            f"🎉 {name}님, 승률 {rate:.1f}% 달성!\n\n"
            "기념촬영을 시작하겠습니다.\n"
            "확인을 누르면 카운트다운이 시작됩니다.")

        # 4) 확인 후 촬영 시작 (탭 이동 + 카운트다운)
        self.start_photo_sequence(name, rate)

    # =====================================================
    # 기념사진 촬영
    # =====================================================
    def start_photo_sequence(self, name, rate):
        """기념사진 탭으로 이동해서 카메라를 켜고 카운트다운을 시작"""
        self.photo_ctx = (name, rate)
        self.last_image = None
        self.set_game_enabled(False)
        self.tabWidget.setCurrentWidget(self.tabPhoto)
        self.lblPhotoTitle.setText(
            f"🎉 {name}님 승률 {rate:.1f}% - 최고 승률 경신! 카메라를 봐주세요")
        self.lblPhotoInfo.setText("")

        if not self.camera.open():                 # 실패 시 안내문구만 보여주고 계속 진행
            self.lblCamera.setText(self.camera.error)

        self.count = config.COUNTDOWN_START
        self.lblCountdown.setText(str(self.count))
        self.count_timer.start(1000)   # 1초마다 숫자 감소
        self.preview_timer.start(33)   # 미리보기 갱신

    def on_count_tick(self):
        """1초마다 호출: 숫자를 줄이다가 0이 되면(= 1이 보이고 1초 뒤) 촬영"""
        self.count -= 1
        if self.count > 0:
            self.lblCountdown.setText(str(self.count))
        else:
            self.count_timer.stop()
            self.take_photo()

    def update_preview(self):
        """카운트다운 동안 카메라 화면을 실시간으로 표시"""
        image = self.camera.read_frame()
        if image is not None:
            self.last_image = image
            self.show_image(image)

    def show_image(self, image):
        """이미지를 lblCamera 크기에 맞춰(비율 유지) 표시"""
        pix = QPixmap.fromImage(image).scaled(
            self.lblCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lblCamera.setPixmap(pix)

    def take_photo(self):
        """촬영 -> 꾸미기 -> 저장 -> 랭킹에 사진 연결 -> 버튼 다시 활성화"""
        self.preview_timer.stop()
        name, rate = self.photo_ctx
        self.lblCountdown.setText("📸")

        # 촬영 우선순위: 지금 프레임 > 마지막 미리보기 프레임 > 기념 카드
        image = self.camera.read_frame()
        if image is None:
            image = self.last_image
        if image is None:
            image = photo_utils.make_fallback_image()
        self.camera.close()

        image = photo_utils.decorate(image, name, rate)
        rel_path = photo_utils.save_photo(image, self.store.photo_dir)

        self.store.set_photo(name, rel_path)
        self.refresh_ranking()

        self.show_image(image)
        self.lblPhotoInfo.setText(f"✅ 기념사진 저장 완료: {rel_path}  (랭킹 탭에서 확인하세요)")
        self.set_game_enabled(True)

    # =====================================================
    # 랭킹
    # =====================================================
    def refresh_ranking(self):
        """랭킹 표와 대결 탭의 '현재 1위' 문구를 다시 그린다"""
        items = self.store.top()
        self.rank_table.refresh(items)
        self.update_top_label(items)

    def update_top_label(self, items):
        cond = (f"기념사진 조건: 승률 {config.MIN_RATE:.0f}% 이상 + "
                f"본인 최고 승률 경신 (최소 {config.MIN_GAMES}판)")
        if items:
            name, e = items[0]
            self.lblTopRate.setText(f"🏆 현재 1위: {name} {e['best_rate']:.1f}%\n{cond}")
        else:
            self.lblTopRate.setText(f"현재 1위 기록 없음\n{cond}")

    def reset_ranking(self):
        """'랭킹 초기화' 버튼: 확인 후 storage/ranking.json 과 photos 폴더를 삭제"""
        if self.count_timer.isActive():   # 촬영 카운트다운 중에는 무시
            return

        answer = QtWidgets.QMessageBox.question(
            self, "랭킹 초기화",
            "랭킹 기록과 저장된 기념사진이 모두 삭제됩니다.\n계속할까요?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if answer != QtWidgets.QMessageBox.Yes:
            return

        self.store.clear()

        # 기념사진 탭 화면도 초기 상태로
        self.lblCamera.clear()
        self.lblCamera.setText("아직 촬영 전입니다")
        self.lblCountdown.setText("-")
        self.lblPhotoInfo.setText("")

        self.refresh_ranking()

    # =====================================================
    def closeEvent(self, event):
        """창을 닫을 때 카메라를 확실히 해제"""
        self.camera.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RPSWindow()
    window.show()
    sys.exit(app.exec_())
