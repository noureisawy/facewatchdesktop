import sys
from PySide2 import *
from ui_interface import Ui_MainWindow
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
from SystemTray import SystemTray
from user.User import User
from LabelingData.LabelingData import LabelingData
from Background.ShareDataThread import ShareDataThread
from Reporting.ReportData import ReportData


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

        # Data Analysis selection compo box on change
        self.ui.dataAnalysisSelection.currentIndexChanged.connect(
            self.handle_data_analysis_selection_change
        )

        # on change date time start and time end
        self.ui.dateTimeStart.dateTimeChanged.connect(self.update_data)
        self.ui.dateTimeEnd.dateTimeChanged.connect(self.update_data)
        self.emotionData = EmotionData(self.ui.dateTimeStart, self.ui.dateTimeEnd)
        self.tirednessData = TirednessData(self.ui.dateTimeStart, self.ui.dateTimeEnd)
        self.selectedData = self.emotionData
        self.ui.lineChart = LineChart(self.ui.lineChartPage, self.selectedData)
        self.ui.scatterPlot = ScatterPlot(self.ui.scatterPlotPage, self.selectedData)
        self.ui.pieChart = PieChart(self.ui.pieChartPage, self.selectedData)
        self.ui.barChart = BarChart(self.ui.barChartPage, self.selectedData)

        # Refresh data when refresh button clicked
        self.ui.refreshBtn.clicked.connect(self.refresh_data)

        # Emotion Gallery Page

        # hide alertness widget
        self.ui.alertnessWid.hide()
        self.ui.selectGalleryComp.currentIndexChanged.connect(
            self.handle_select_gallery_change
        )
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
        self.ui.tiredBtn.clicked.connect(
            lambda: self.refresh_emotional_gallery("tired")
        )
        self.ui.alertBtn.clicked.connect(
            lambda: self.refresh_emotional_gallery("alert")
        )
        self.ui.non_vigilantBtn.clicked.connect(
            lambda: self.refresh_emotional_gallery("non_vigilant")
        )

        # notification
        self.ui.notifyMe.setChecked(True)
        notification = Notification(tray, True)
        self.ui.notifyMe.toggled.connect(self.handle_checkbox_notify_me_changed)

        # Settings Page

        # run face watch background task
        self.faceWatchTask = FaceWatchTask(
            interval=self.ui.watchInt.currentText(), notification=notification
        )
        self.faceWatchTask.started.connect(lambda: print("face watch task is started"))
        self.faceWatchTask.finished.connect(
            lambda: print("face watch task is finished")
        )
        # TODO: uncomment this line to start face watch task
        self.faceWatchTask.start_task()
        self.ui.watchMe.setChecked(True)

        # trigger watch me checkbox
        self.ui.watchMe.toggled.connect(self.handle_checkbox_watch_me_changed)

        # combobox changed
        self.ui.watchInt.currentTextChanged.connect(
            self.handle_interval_combobox_changed
        )

        # Profile Page
        self.user = User(self)

        # Labeling Page
        self.labelingData = LabelingData(
            self.ui.labelingDataContainer,
            self.ui.labelingImageContainer,
            self.ui.lowerLabeling,
        )
        self.ui.emotionsBtn.clicked.connect(
            lambda: self.labelingData.set_label("emotions")
        )
        self.ui.alertnessBtn.clicked.connect(
            lambda: self.labelingData.set_label("alertness")
        )
        self.ui.mentalHealthBtn.clicked.connect(
            lambda: self.labelingData.set_label("mental_health")
        )
        self.ui.symptomsBtn.clicked.connect(
            lambda: self.labelingData.set_label("symptoms")
        )
        self.ui.closeImageLabelingContainer.clicked.connect(
            lambda y: self.ui.lowerLabeling.collapseMenu()
        )
        self.ui.shareBtn.clicked.connect(self.share_data)

        # Report Page
        self.reportData = ReportData(self.ui.reportsDataContainer)

    def share_data(self):
        self.ui.shareBtn.setEnabled(False)
        self.ui.shareBtn.setText("Sharing...")
        QApplication.processEvents()

        self.share_thread = ShareDataThread()
        self.share_thread.finished.connect(lambda: self.on_share_finished())
        self.share_thread.error.connect(lambda message: self.on_share_error(message))
        self.share_thread.start()

    def on_share_finished(self):
        self.ui.shareBtn.setText("Share")
        self.ui.shareBtn.setEnabled(True)
        QMessageBox.information(None, "Success", "Images sent successfully")

    def on_share_error(self, message):
        self.ui.shareBtn.setText("Share")
        self.ui.shareBtn.setEnabled(True)
        QMessageBox.warning(None, "Error", message)

    def handle_select_gallery_change(self, index):
        if index == 0:
            self.refresh_emotional_gallery("neutral")
            self.ui.alertnessWid.hide()
            self.ui.emotionWid.show()
        elif index == 1:
            self.refresh_emotional_gallery("alert")
            self.ui.emotionWid.hide()
            self.ui.alertnessWid.show()

    def handle_data_analysis_selection_change(self, index):
        if index == 0:
            self.selectedData = self.emotionData
        elif index == 1:
            self.selectedData = self.tirednessData
        self.update_data()

    def handle_interval_combobox_changed(self, text):
        self.faceWatchTask.interval = text

    def handle_checkbox_notify_me_changed(self, checked):
        if checked:
            self.faceWatchTask.notification = Notification(tray, True)
        else:
            self.faceWatchTask.notification = Notification(tray, False)

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
        self.tirednessData.refresh_data(self.ui.dateTimeStart, self.ui.dateTimeEnd)
        self.ui.lineChart.set_data(self.selectedData)
        self.ui.scatterPlot.set_data(self.selectedData)
        self.ui.pieChart.set_data(self.selectedData)
        self.ui.barChart.set_data(self.selectedData)


def handle_labeling_action():
    window.show()
    window.ui.rightMenuContainer.expandMenu()
    window.ui.rightMenuPages.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # TODO: fix this
    # app.setQuitOnLastWindowClosed(False)
    # tray icon

    tray = SystemTray(parent=app)
    tray.show()
    window = MainWindow()
    tray.action_hide.triggered.connect(window.hide)
    tray.action_show.triggered.connect(window.show)
    tray.labeling_action.triggered.connect(handle_labeling_action)

    sys.exit(app.exec_())
