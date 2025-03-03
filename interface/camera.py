import cv2
from utility import config


def take_picture(file_path):
    camera = cv2.VideoCapture(0)
    _, frame = camera.read()
    cv2.imwrite(file_path, frame)
    camera.release()
    print("|-- Photo captured")
