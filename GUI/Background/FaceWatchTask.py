from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import cv2
from deepface import DeepFace
from DB.Data import Data
import time
from PyQt5.QtWidgets import QMessageBox


class FaceWatchTask(QThread):
    finished = pyqtSignal()
    started = pyqtSignal()

    def __init__(self, interval, notification):
        self.is_taking_image = True
        self.is_running = True
        self.interval = interval
        self.notification = notification
        super().__init__()

    def take_photo(self):
        try:
            cap = cv2.VideoCapture(1)
        except Exception as e:
            print(e)
            QMessageBox.warning("Error", "Camera not found")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        ret, frame = cap.read()
        cap.release()
        try:
            self.analyze_frame(frame)
        except Exception as e:
            print(e)

    def analyze_frame(self, frame):
        sub_file_name = "neutral"
        analysis = DeepFace.analyze(frame, actions=["emotion"])
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
        self.notification.show_notification(analysis[0]["dominant_emotion"])
        print(analysis[0])
        self.data.insert_emotion(analysis[0])
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

    @pyqtSlot()
    def start_task(self):
        self.is_running = True
        self.started.emit()
        self.start()

    @pyqtSlot()
    def stop_task(self):
        self.is_running = False

    def run(self):  # sourcery skip: avoid-builtin-shadow
        self.data = Data()
        while self.is_running:
            map = {
                "": 1,
                "15 sec": 15,
                "1 min": 1 * 60,
                "2 min": 2 * 60,
                "3 min": 3 * 60,
                "5 min": 5 * 60,
                "10 min": 10 * 60,
                "15 min": 15 * 60,
                "30 min": 30 * 60,
                "1 h": 60 * 60,
            }
            if self.is_taking_image:
                self.take_photo()
            timeInt = map.get(self.interval, 1)
            time.sleep(timeInt)
        self.data.conn.conn.close()
        self.finished.emit()

