
# test the background task

from Background.FaceWatchTask import FaceWatchTask
# import qsystemtrayicon
import time
# test FaceWatchTask class

def test_FaceWatchTask():
    print("test_FaceWatchTask")
    task = FaceWatchTask()
    task.start_task()
    time.sleep(1000)
    task.stop_task()

test_FaceWatchTask()
