import cv2
import datetime
import os
import time
import win32serviceutil
import win32service
import win32event

class ImageCaptureService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'ImageCaptureService'
    _svc_display_name_ = 'Image Capture Service'
    _svc_description_ = 'Captures an image every 15 minutes and saves it to a file.'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        while True:
            # Capture an image
            self.capture_image()

            # Wait 15 minutes before capturing the next image
            win32event.WaitForSingleObject(self.hWaitStop, 15 * 60 * 1000)  # Wait 15 minutes (900 seconds)

    def capture_image(self):
        # Open the default camera
        cap = cv2.VideoCapture(0)

        # Set the resolution of the camera capture
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Capture a frame from the camera
        ret, frame = cap.read()

        # Save the captured frame to a file
        filename = f"photo_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        cv2.imwrite(filename, frame)

        # Release the camera capture and close the window
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ImageCaptureService)

    