"""앱 전역 설정값 / 경로 / 화면 표시용 상수 모음.

숫자나 경로를 바꾸고 싶을 때는 이 파일만 수정하면 됩니다.
"""
import os

# ---------------- 게임 / 촬영 규칙 ----------------
MIN_RATE = 25.0         # 기념사진 촬영 최소 승률(%)
MIN_GAMES = 5           # 승률 판정을 시작하는 최소 대결 수 (1판 1승 = 100% 방지, 1이면 제한 없음)
COUNTDOWN_START = 5     # 촬영 카운트다운 시작 숫자 (5 -> 4 -> 3 -> 2 -> 1 -> 촬영)
MAX_RANK = 10           # 랭킹에 보여줄 최대 인원

# ---------------- 경로 ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # 프로젝트 최상위 폴더
UI_FILE = os.path.join(BASE_DIR, "gui.ui")               # Qt Designer UI 파일
PHOTO_DIR_NAME = "photos"                                # JSON에는 이 상대 경로로 저장
PHOTO_DIR = os.path.join(BASE_DIR, PHOTO_DIR_NAME)       # 기념사진 저장 폴더
RANK_FILE = os.path.join(BASE_DIR, "storage", "ranking.json")  # 랭킹 데이터 파일

# ---------------- 화면 표시용 ----------------
# 결과 -> (표시 문구, 글자 색상)
RESULT_STYLE = {
    "승리": ("🎉 승리!", "#2e9e4f"),
    "패배": ("😢 패배...", "#d9534f"),
    "무승부": ("🤝 무승부", "#888888"),
}
MEDALS = ["🥇", "🥈", "🥉"]   # 랭킹 1~3위 아이콘
