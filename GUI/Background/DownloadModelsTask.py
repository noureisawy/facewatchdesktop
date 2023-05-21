import subprocess
import time
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class DownloadModelsTask(QThread):
    finished = pyqtSignal()
    started = pyqtSignal()

    def __init__(self):
        self.is_running = True
        super().__init__()

    @pyqtSlot()
    def start_task(self):
        self.is_running = True
        self.started.emit()
        self.start()

    @pyqtSlot()
    def stop_task(self):
        self.is_running = False

    def download_models(self):
        try:
            subprocess.run(
                [
                    "git",
                    "-C",
                    "Models/",
                    "clone",
                    "https://github.com/abdelrahmanfekri/facewatchmodels.git",
                ]
            )
        except Exception as e:
            print(e)
        subprocess.run(["git", "-C", "Models/facewatchmodels/", "pull", "origin", "main"])

    def run(self):
        while self.is_running:
            self.download_models()
            # sleep one day
            time.sleep(24 * 60 * 60)
        self.finished.emit()
