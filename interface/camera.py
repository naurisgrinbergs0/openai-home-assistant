import cv2
import utility.config as config


def take_picture(file_path):
    camera = cv2.VideoCapture(0)
    _, frame = camera.read()
    cv2.imwrite(file_path, frame)
    camera.release()
    print("|-- Photo captured")
