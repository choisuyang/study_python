# ✌️✊✋ 가위바위보 게임 (PyQt5)

컴퓨터와 가위바위보를 하고, 전적을 대시보드로 확인하며,
**승률 신기록을 세우면 웹캠으로 기념사진을 찍어 랭킹에 남기는** 데스크톱 앱입니다.

## 주요 기능

| 탭 | 설명 |
|---|---|
| 📊 대시보드 | 총 대결 / 승 / 패 / 무 수와 승률(%)을 한눈에 확인 |
| ⚔️ 대결 | 가위·바위·보 버튼으로 컴퓨터(랜덤)와 대결, 오른쪽에 대결 기록(히스토리), 하단에 승률과 현재 1위 승률 표시 |
| 📸 기념사진 | 조건 달성 시 자동 이동 → 5초부터 1초까지 카운트다운 → 1초 뒤 촬영 |
| 🏆 랭킹 | 최고 승률 순 TOP 10, 승률 옆에 기념사진 썸네일 (클릭하면 크게 보기) |

### 기념사진 촬영 조건

아래 조건을 **모두** 만족하면 기념사진 탭으로 이동해 촬영합니다.

1. 현재 승률이 **30% 이상**
2. 현재 승률이 랭킹 **1위의 승률보다 높음**
3. 대결 수가 **최소 5판 이상** (1판 1승 = 100% 같은 경우를 방지)

> 5판 제한은 `main.py` 상단의 `MIN_GAMES` 값으로 조정할 수 있습니다. (`1`로 바꾸면 제한 없음)

촬영 중에는 대결 버튼이 잠시 비활성화되고, 촬영이 끝나면 다시 활성화됩니다.
카메라가 없거나 `opencv-python`이 설치되지 않은 경우에는 웹캠 대신 **"WINNER!" 기념 카드**가 저장됩니다.

## 파일 구성

```
.
├── main.py            # 메인 프로그램
├── gui.ui             # Qt Designer UI 파일
├── requirements.txt   # 설치 패키지 목록
├── README.md
├── ranking.json       # (자동 생성) 랭킹 데이터
└── photos/            # (자동 생성) 기념사진 저장 폴더
```

## 설치 방법

Python **3.8 이상**이 필요합니다.

```bash
# 1) (선택) 가상환경
python -m venv venv
venv\Scripts\activate           # Windows
source venv/bin/activate        # macOS / Linux

# 2) 패키지 설치
pip install -r requirements.txt
```

직접 설치하려면 아래 두 줄이면 됩니다.

```bash
pip install PyQt5
pip install opencv-python
```

## 실행 방법

`main.py`와 `gui.ui`를 **같은 폴더**에 두고 실행하세요.

```bash
python main.py        # macOS / Linux 에서 python 이 안 되면 python3 main.py
```

## 사용 방법

1. **⚔️ 대결 탭**에서 플레이어 이름을 입력합니다. (첫 대결 후에는 잠기며, `기록 초기화`를 누르면 다시 변경 가능)
2. ✌️ 가위 / ✊ 바위 / ✋ 보 버튼을 눌러 대결합니다.
3. 승률이 조건을 만족하면 📸 기념사진 탭으로 자동 이동하고 카운트다운이 시작됩니다.
4. 🏆 랭킹 탭에서 TOP 10과 기념사진을 확인합니다.

## 데이터 초기화

랭킹을 완전히 지우려면 앱을 종료한 뒤 `ranking.json` 파일과 `photos/` 폴더를 삭제하세요.

## 문제 해결

| 증상 | 해결 방법 |
|---|---|
| `ModuleNotFoundError: No module named 'PyQt5'` | `pip install PyQt5` 실행 (가상환경 활성화 여부 확인) |
| `FileNotFoundError: gui.ui` | `gui.ui`가 `main.py`와 같은 폴더에 있는지 확인 |
| 카메라가 켜지지 않음 | 다른 프로그램(화상회의 등)이 카메라를 쓰고 있는지 확인 |
| macOS에서 카메라 접근 불가 | 시스템 설정 → 개인정보 보호 및 보안 → 카메라에서 터미널(또는 사용하는 IDE) 허용 |
| Windows에서 카메라 접근 불가 | 설정 → 개인정보 및 보안 → 카메라에서 데스크톱 앱 접근 허용 |
| Linux에서 `xcb` 관련 오류 | `sudo apt install libxcb-xinerama0 libxcb-cursor0` |
| 카메라 대신 "WINNER!" 카드가 저장됨 | 카메라 연결/권한 또는 `pip install opencv-python` 확인 |
| 이모지가 네모로 보임 | OS에 이모지 폰트가 없는 경우. Windows 10+, macOS는 보통 정상 |

## PyQt6로 실행하려면

- `main.py`의 `PyQt5`를 `PyQt6`로 변경
- `app.exec_()` → `app.exec()`, `dlg.exec_()` → `dlg.exec()`
- Enum 경로가 달라집니다. 예: `Qt.AlignCenter` → `Qt.AlignmentFlag.AlignCenter`, `QImage.Format_RGB888` → `QImage.Format.Format_RGB888`

PyQt5를 그대로 쓰는 것을 권장합니다.
