import time
from SMWinservice import SMWinservice
import cv2
import os
current_dir = os.getcwd()
print(" directory ",current_dir)


class FaceWatchService(SMWinservice):
    _svc_name_ = "FaceWatchService"
    _svc_display_name_ = "Face Watch Service"
    _svc_description_ = "Face service serves face watch application"

    def start(self, argv=("",)):
        self.map = {
            "": 1,
            "15 sec": 15,
            "15 min": 13 * 60,
            "30 min": 30 * 60,
            "1 h": 60 * 60,
        }
        arg1 = argv[1] if len(argv) > 1 else ""
        self.interval = self.map[arg1]
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        self.interval = 15
        while self.isrunning:
            take_photo()
            time.sleep(self.interval)


def take_photo():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 48)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 48)
    ret, frame = cap.read()
    cap.release()
    filename = f'C:/Users/UG/Desktop/research/FaceWatch/Images/image{time.strftime("%Y%m%d-%H%M%S")}.jpg'
    cv2.imwrite(filename, frame)


if __name__ == "__main__":
    FaceWatchService.parse_command_line()
    # take_photo()
