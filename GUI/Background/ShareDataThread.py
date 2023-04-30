from PyQt5.QtCore import QThread, pyqtSignal
import requests
from constants import dir_name, server_url
from DB.Data import Data


class ShareDataThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.data = Data()
        self.data_dict = {
            "emotions": self.data.get_all_emotions_labeling,
            "alertness": self.data.get_all_tiredness_labeling,
            "mental_health": self.data.get_all_mental_health_labeling,
            "symptoms": self.data.get_all_symptoms_concerns_labeling,
        }
        images = []
        labels = []
        noImages = 0
        flag = True
        image_chunk = 10
        for label, data in self.data_dict.items():
            for row in data():
                data_shared_before = self.data.check_if_data_shared_before(
                    row[1], row[2]
                )
                if data_shared_before:
                    continue
                labels.append(row[1])
                images.append(f"{label}_label/{row[2]}.jpg")
                self.data.insert_shared_data(row[1], row[2])
                noImages += 1
                if noImages % image_chunk == 0:
                    flag = self.send_images(images, labels)
                    images = []
                    labels = []
                    if not flag:
                        break
            if not flag:
                break

        if flag:
            self.finished.emit()
        else:
            self.error.emit("Error sending images")

    def send_images(self, images, labels):
        url = f"{server_url}/labeling/receive_images/"
        files = [
            ("images", open(f"{dir_name}/{image_path}", "rb")) for image_path in images
        ]
        data = {"labels": labels}
        response = requests.post(url, files=files, data=data)
        return response.status_code == 200