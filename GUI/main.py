import sys
from PySide2 import *
from ui_interface import *
import win32serviceutil
import win32service
from PyQt5.QtCore import QDateTime
from DataAnalysis.LineChart import LineChart
from DataAnalysis.ScatterPlot import ScatterPlot
from DataAnalysis.PieChart import PieChart
from DataAnalysis.BarChart import BarChart
from DataAnalysis.EmotionData import EmotionData
from Custom_Widgets.Widgets import *
from EmotionGallery.ReadImages import ReadImages
from Background.FaceWatchTask import FaceWatchTask
from Background.Notification import Notification
from DataAnalysis.TirednessData import TirednessData


class MainWindow(QMainWindow):
    def __init__(self):
        self.service_name = "FaceWatchService"
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        loadJsonStyle(self, self.ui)
        self.show()

        # EXPAND CENTER MENU WIDGET SIZE
        self.ui.settingsBtn.clicked.connect(
            lambda: self.ui.centerMenuContainer.expandMenu()
        )
        self.ui.infoBtn.clicked.connect(
            lambda: self.ui.centerMenuContainer.expandMenu()
        )
        self.ui.helpBtn.clicked.connect(
            lambda: self.ui.centerMenuContainer.expandMenu()
        )

        #  COLLAPSE CENTER MENU WIDGET SIZE
        self.ui.closeCenterMenuBtn.clicked.connect(
            lambda: self.ui.centerMenuContainer.collapseMenu()
        )

        # EXPAND Right MENU WIDGET SIZE
        self.ui.notBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.profileBtn.clicked.connect(
            lambda: self.ui.rightMenuContainer.expandMenu()
        )

        #  COLLAPSE Right MENU WIDGET SIZE
        self.ui.closeRightMenu.clicked.connect(
            lambda: self.ui.rightMenuContainer.collapseMenu()
        )

        # Data Analysis Page
        self.ui.dateTimeEnd.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeStart.setDateTime(
            QDateTime.currentDateTime().addSecs(-3600 * 24)
        )

        # on change date time start and time end
        self.ui.dateTimeStart.dateTimeChanged.connect(self.update_data)
        self.ui.dateTimeEnd.dateTimeChanged.connect(self.update_data)
        self.emotionData = EmotionData(self.ui.dateTimeStart, self.ui.dateTimeEnd)
        self.tirednessData = TirednessData(self.ui.dateTimeStart, self.ui.dateTimeEnd)
        self.ui.lineChart = LineChart(self.ui.lineChartPage, self.emotionData)
        self.ui.scatterPlot = ScatterPlot(self.ui.scatterPlotPage, self.emotionData)
        self.ui.pieChart = PieChart(self.ui.pieChartPage, self.emotionData)
        self.ui.barChart = BarChart(self.ui.barChartPage, self.emotionData)

        # Refresh data when refresh button clicked
        self.ui.refreshBtn.clicked.connect(self.refresh_data)

        # Emotion Gallery Page
        self.readImage = ReadImages("neutral", self.ui.emotionListImages)
        self.ui.neutralBtn.clicked.connect(
            lambda: self.refresh_emotional_gallery("neutral")
        )
        self.ui.happyBtn.clicked.connect(
            lambda: self.refresh_emotional_gallery("happy")
        )
        self.ui.sadBtn.clicked.connect(lambda: self.refresh_emotional_gallery("sad"))
        self.ui.angryBtn.clicked.connect(
            lambda: self.refresh_emotional_gallery("angry")
        )
        self.ui.fearBtn.clicked.connect(lambda: self.refresh_emotional_gallery("fear"))
        self.ui.disgustBtn.clicked.connect(
            lambda: self.refresh_emotional_gallery("disgust")
        )
        self.ui.surpriseBtn.clicked.connect(
            lambda: self.refresh_emotional_gallery("surprise")
        )

        # action hide and show
        action_hide.triggered.connect(self.hide)
        action_show.triggered.connect(self.showNormal)

        # notification
        notification = Notification(tray)

        # Settings Page

        # run face watch background task
        self.faceWatchTask = FaceWatchTask(
            interval=self.ui.watchInt.currentText(), notification=notification
        )
        self.faceWatchTask.started.connect(lambda: print("face watch task is started"))
        self.faceWatchTask.finished.connect(
            lambda: print("face watch task is finished")
        )
        self.faceWatchTask.start_task()
        self.ui.watchMe.setChecked(True)

        # trigger watch me checkbox
        self.ui.watchMe.toggled.connect(self.handle_checkbox_watch_me_changed)

        # combobox changed
        self.ui.watchInt.currentTextChanged.connect(
            self.handle_interval_combobox_changed
        )

    def handle_interval_combobox_changed(self, text):
        print(text)
        self.faceWatchTask.interval = text

    def handle_checkbox_watch_me_changed(self, checked):
        if checked:
            self.faceWatchTask.start_task()
        else:
            self.faceWatchTask.stop_task()

    def refresh_emotional_gallery(self, emotion):
        self.ui.emotionListImages.clear()
        self.readImage.refresh(emotion)

    def refresh_data(self):
        self.ui.dateTimeEnd.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeStart.setDateTime(
            QDateTime.currentDateTime().addSecs(-3600 * 24)
        )
        self.update_data()

    def update_data(self, *args):
        self.emotionData.refresh_data(self.ui.dateTimeStart, self.ui.dateTimeEnd)
        self.ui.lineChart.set_data(self.emotionData)
        self.ui.scatterPlot.set_data(self.emotionData)
        self.ui.pieChart.set_data(self.emotionData)
        self.ui.barChart.set_data(self.emotionData)

    def get_auto_start(self):
        return (
            win32serviceutil.QueryServiceConfig(self.service_name)[1]["start_type"]
            == win32service.SERVICE_AUTO_START
        )


def show_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowIcon(QIcon("public/logo.png"))

    msg.setWindowTitle(" Message Box")
    msg.setText("This is a message for you")

    msg.setInformativeText("Additional information can be put here")
    msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()


def show_tray_message(tray):
    notificationTitle = "Notification Title"
    notificationMessage = "Notification Message"
    icon = QIcon("public/logo.png")
    duration = 3 * 1000
    tray.showMessage(notificationTitle, notificationMessage, icon, duration)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(
            None,
            "Systray",
            "I couldn't detect any system tray on this system.",
        )
        sys.exit(1)

    app.setQuitOnLastWindowClosed(False)

    tray = QSystemTrayIcon(QIcon("public/logo.png"), app)
    tray.setToolTip("FaceWatch")

    # tray icon menu
    menu = QMenu()
    action_hide = QAction("Hide Window")
    menu.addAction(action_hide)

    action_show = QAction("Show Window")
    menu.addAction(action_show)

    action_exit = QAction("Exit")
    action_exit.triggered.connect(sys.exit)
    menu.addAction(action_exit)

    tray.setContextMenu(menu)
    tray.show()

    window = MainWindow()
    sys.exit(app.exec_())
