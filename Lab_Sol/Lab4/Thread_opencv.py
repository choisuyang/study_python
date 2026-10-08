import sys, cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtGui import QImage


class CameraThread(QThread):
    send_image = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._run_flag = False
        self.cap = None

    def init_capture(self):
        cameras = QCameraInfo.availableCameras()
        if not cameras:
            print("연결된 카메라 장치가 없습니다!")
            return -1

        print("=== 발견된 카메라 장치 목록 ===")
        for i, cam in enumerate(cameras):
            print(f"Index [{i}] : {cam.description()}")
        print("===============================")

        target_index = 0
        if len(cameras) > target_index:
            print(f"현재 선택된 카메라: {cameras[target_index].description()}")
            return target_index
        else:
            print("지정한 카메라 인덱스를 찾을 수 없어 기본 0번을 사용합니다.")
            return 0
        
    def run(self):
        target = self.init_capture()
        if target < 0:
            print("Error : 쓰레드 종료 - 카메라 선택 안됨")
            return  

        self.cap = cv2.VideoCapture(target, cv2.CAP_DSHOW)
        
        if not self.cap.isOpened():
            print(f"Error: 카메라 인덱스 [{target}]를 열 수 없습니다.")
            return  
        
        self._run_flag = True
        print("쓰레드 Start")
        
        while self._run_flag:
            ret, cv_img = self.cap.read()
            if ret:
                # 1. OpenCV는 기본적으로 색상 순서가 BGR(파랑-초록-빨강) 
                #    PyQt가 올바른 색상(RGB)으로 인식할 수 있도록 변환
                rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                # 2. 변환된 이미지 배열에서 높이(h), 너비(w), 채널 수(ch, 컬러는 보통 3)를 가져옴
                h, w, ch = rgb_image.shape
                # 3. 이미지 한 줄을 구성하는 데 필요한 전체 바이트 수(너비 × 채널 수)를 계산
                #    QImage(data, width, height, bytesPerLine, format)를 전달 받음
                bytes_per_line = ch * w
                # 4. 넘파이(NumPy) 배열 형태의 이미지 데이터를 PyQt가 다룰 수 있는 QImage 객체로 변환
                #    마지막 인자(QImage.Format_RGB888)는 픽셀당 8비트씩 RGB 3채널 형식을 의미
                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                # 5. QLabel 크기에 맞추기 위해 640x480 해상도로 조절하되, 
                #    원본 영상의 가로세로 비율(Aspect Ratio)이 찌그러지지 않도록 유지하며 스케일링
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                
                self.send_image.emit(p)
            else:
                print("Warning: 프레임을 읽어오지 못했습니다.")
                break
                
        if self.cap and self.cap.isOpened():
            self.cap.release()
        print("카메라 자원 해제 완료")

    def stop(self):
        self._run_flag = False
        self.wait()
        print("스레드 안전 종료 완료")