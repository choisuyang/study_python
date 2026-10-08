# ✌️✊✋ 가위바위보 게임 (PyQt5)

컴퓨터와 가위바위보를 하고, 승률이 오르면 웹캠으로 기념사진을 찍어 랭킹에 남기는 앱입니다.

## 폴더 구조

```
rps_game/
├── main.py                    # 진입점 + 메인 윈도우 (화면 연결 / 흐름 제어)
├── config.py                  # 설정값(최소 승률 등), 경로, 표시용 상수
├── gui.ui                     # Qt Designer UI 파일
├── requirements.txt
├── core/
│   └── game.py                # 가위바위보 규칙, 전적(승/패/무, 승률) 계산
├── storage/
│   ├── ranking_store.py       # ranking.json 저장 / 조회 / 정렬 / 삭제
│   └── ranking.json           # (자동 생성) 랭킹 데이터
├── camera/
│   ├── camera_service.py      # 웹캠 열기 / 프레임 읽기 / 닫기
│   └── photo_utils.py         # 기념사진 꾸미기 / 대체 카드 / 저장
├── ui/
│   └── rank_table.py          # 랭킹 탭 표 UI + 사진 확대 팝업
└── photos/                    # (자동 생성) 기념사진
```

## 설치 / 실행

Python 3.8 이상 필요. 

```bash
pip install -r requirements.txt   # PyQt5, opencv-python
python main.py
```

> `main.py`를 **rps_game 폴더 안에서** 실행하세요. (하위 폴더 모듈과 gui.ui를 이 위치 기준으로 찾습니다.)

## 기념사진 촬영 규칙

1. 현재 승률이 `MIN_RATE`(기본 25%) 이상
2. 해당 플레이어의 **본인 최고 승률을 경신**
3. 대결 수가 `MIN_GAMES`(기본 5판) 이상

조건을 달성하면 버튼이 잠기고 알림창이 뜹니다. 확인을 누르면 📸 기념사진 탭에서 5→1 카운트다운 후 촬영합니다.
카메라가 없으면 "WINNER!" 기념 카드가 대신 저장됩니다. 설정값은 `config.py`에서 바꿀 수 있습니다.

## 어디를 고치면 되나요?

| 하고 싶은 것 | 수정 파일 |
|---|---|
| 최소 승률 / 최소 판수 / 카운트다운 / 랭킹 인원 변경 | `config.py` |
| 가위바위보 규칙, 승률 계산 방식 변경 | `core/game.py` |
| 랭킹 저장 형식, 정렬 기준 변경 | `storage/ranking_store.py` |
| 카메라 설정 / 사진 꾸미기(문구, 띠 색) 변경 | `camera/` |
| 랭킹 표 모양 변경 | `ui/rank_table.py` |
| 화면 흐름(버튼 동작, 탭 이동) 변경 | `main.py` |

## 데이터 초기화

앱의 🏆 랭킹 탭 → `랭킹 초기화` 버튼, 또는 `storage/ranking.json`과 `photos/` 폴더를 직접 삭제하세요.

## 문제 해결

| 증상 | 해결 |
|---|---|
| `ModuleNotFoundError: No module named 'config'` | `rps_game` 폴더 안에서 `python main.py` 실행 |
| `ModuleNotFoundError: PyQt5` | `pip install PyQt5` |
| 카메라가 안 켜짐 | 다른 프로그램의 카메라 사용 여부 / OS 카메라 권한 확인 |
| "WINNER!" 카드가 저장됨 | 카메라 연결 또는 `pip install opencv-python` 확인 |
