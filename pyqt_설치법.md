# PyQt 설치법

## 1. Python 설치
python 3.11 버전을 설치

## 2. PyQt5 설치
명령 실행창에서 다음 명령을 차례대로 입력합니다.
```bash	
pip upgrade : python -m pip install --upgrade pip
pip install PyQt5
pip install pyqt5Designer
pip install PyQt5-stubs
```
## 3. QtDesigner 경로
자신의 python이 설치된 폴더\Lib\site-packages\QtDesigner 폴더
- 경로확인법 : 명령프롬프트에서 실행
1. `where python` 명령을 실행하여 Python 설치 경로를 확인
2. python 실행 후 다음 입력
```python
>> import sys
>> sys.executable
```
## 4. Qt platform plugin could be initialized 오류시
- 환경변수에 Qt plugin 경로가 없어서 발생 : 환경 변수에 추가 필요
- 환경변수 설정에서 Qt plugin 경로를 추가해야 함
  - 변수 이름 : QT_QPA_PLATFORM_PLUGIN_PATH
  - 변수 값 : 파이썬 경로\Lib\site-packages\PyQt5\Qt\plugins\platforms
    - …\Qt 라는 폴더명 대신 다른 폴더명으로 존재하는 경우도 있음


