import time
from SMWinservice import SMWinservice
import cv2
import os

from GUI.DB.Data import Data
from deepface import DeepFace

data = Data()
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
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    ret, frame = cap.read()
    cap.release()
    try:
        sub_file_name = "neutral"
        analysis = DeepFace.analyze(frame, actions=["emotion"])
        print(analysis)
        match analysis[0]["dominant_emotion"]:
            case "angry":
                sub_file_name = "angry"
            case "disgust":
                sub_file_name = "disgust"
            case "fear":
                sub_file_name = "fear"
            case "happy":
                sub_file_name = "happy"
            case "sad":
                sub_file_name = "sad"
            case "surprise":
                sub_file_name = "surprise"
            case "neutral":
                sub_file_name = "neutral"
        print(analysis[0])
        data.insert_emotion(analysis[0])
        filename = f'C:/Users/UG/Desktop/research/FaceWatch/Images/{sub_file_name}/{time.strftime("%Y%m%d-%H%M%S")}.jpg'
        # draw rectangle to main image around the face
        cv2.rectangle(
            frame,
            (analysis[0]["region"]["x"], analysis[0]["region"]["y"]),
            (
                analysis[0]["region"]["x"] + analysis[0]["region"]["w"],
                analysis[0]["region"]["y"] + analysis[0]["region"]["h"],
            ),
            (0, 255, 0),
            2,
        )
        # write the emotion of the person
        cv2.putText(
            frame,
            analysis[0]["dominant_emotion"],
            (analysis[0]["region"]["x"], analysis[0]["region"]["y"]),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.imwrite(filename, frame)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    FaceWatchService.parse_command_line()
    # take_photo()
