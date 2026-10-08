"""웹캠 열기 / 프레임 읽기 / 닫기 전담 클래스.

opencv-python 이 없거나 카메라가 없어도 앱이 죽지 않도록
open() 이 False 를 돌려주고, 이유는 self.error 에 담는다.
"""
import sys

from PyQt5.QtGui import QImage

try:
    import cv2
except ImportError:
    cv2 = None


class CameraService:
    def __init__(self):
        self._cap = None
        self.error = ""   # 열기에 실패한 이유 (화면 안내문구로 사용)

    @property
    def is_open(self):
        return self._cap is not None

    def open(self):
        """카메라를 연다. 성공하면 True, 실패하면 False (이유는 self.error)"""
        self._cap = None
        if cv2 is None:
            self.error = "opencv-python 미설치 → 기념 카드로 대체됩니다"
            return False

        # Windows 는 CAP_DSHOW 를 쓰면 카메라가 훨씬 빨리 열린다
        cap = (cv2.VideoCapture(0, cv2.CAP_DSHOW) if sys.platform == "win32"
               else cv2.VideoCapture(0))
        if not cap.isOpened():
            cap.release()
            self.error = "카메라를 찾을 수 없음 → 기념 카드로 대체됩니다"
            return False

        self._cap = cap
        self.error = ""
        return True

    def read_frame(self):
        """현재 프레임을 QImage(RGB)로 돌려준다. 읽기 실패 시 None"""
        if self._cap is None:
            return None
        ok, frame = self._cap.read()
        if not ok:
            return None
        frame = cv2.flip(frame, 1)                    # 거울처럼 좌우 반전
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV(BGR) -> Qt(RGB)
        h, w, ch = rgb.shape
        # .copy() 가 중요: 원본 numpy 메모리가 사라져도 이미지가 유지되도록 복사
        return QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888).copy()

    def close(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None
