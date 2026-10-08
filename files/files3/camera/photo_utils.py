"""기념사진 이미지 만들기 / 꾸미기 / 저장 (카메라와 무관한 이미지 처리)."""
import os
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QImage, QLinearGradient, QPainter

from config import PHOTO_DIR, PHOTO_DIR_NAME


def make_fallback_image():
    """카메라가 없을 때 대신 쓰는 'WINNER!' 기념 카드 (640x480 그라데이션)"""
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


def decorate(image, name, rate):
    """사진 하단에 반투명 띠를 깔고 '이름 / 승률 / 촬영 시각'을 적어 새 이미지로 돌려준다."""
    img = image.convertToFormat(QImage.Format_RGB32)
    w, h = img.width(), img.height()
    p = QPainter(img)

    p.fillRect(0, h - 80, w, 80, QColor(0, 0, 0, 150))   # 하단 반투명 검정 띠
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


def save_photo(image, photo_dir=PHOTO_DIR):
    """이미지를 photos 폴더에 PNG로 저장하고, JSON에 넣을 '상대 경로'를 돌려준다."""
    os.makedirs(photo_dir, exist_ok=True)
    filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image.save(os.path.join(photo_dir, filename))
    return f"{PHOTO_DIR_NAME}/{filename}"
