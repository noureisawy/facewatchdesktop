import time
from SMWinservice import SMWinservice
import cv2

class PythonCornerExample(SMWinservice):
    _svc_name_ = "PythonCornerExample"
    _svc_display_name_ = "Python Corner's Winservice Example"
    _svc_description_ = "That's a great winservice! :)"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        while self.isrunning:
            take_photo()
            time.sleep(1)


def take_photo():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 48)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 48)
    ret, frame = cap.read()
    cap.release()
    filename = f'C:/Users/UG/Desktop/research/FetchWatch/Images/image{time.strftime("%Y%m%d-%H%M%S")}.jpg'
    cv2.imwrite(filename, frame)
    print(ret)
    print(frame.shape)

if __name__ == "__main__":
    PythonCornerExample.parse_command_line()
    #take_photo()
