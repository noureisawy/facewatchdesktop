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

        # Settings Page
        self.ui.watchMe.toggled.connect(self.start_service)
        self.status = win32serviceutil.QueryServiceStatus(self.service_name)[1]
        if self.status == win32service.SERVICE_RUNNING:
            self.ui.watchMe.setChecked(True)
        else:
            self.ui.watchMe.setChecked(False)

        self.ui.dateTimeEnd.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeStart.setDateTime(QDateTime.currentDateTime().addDays(-1))
        # on change date time start and time end
        self.ui.dateTimeStart.dateTimeChanged.connect(self.update_data)
        self.ui.dateTimeEnd.dateTimeChanged.connect(self.update_data)

        # Data Analysis Page
        self.emotionData = EmotionData(self.ui.dateTimeStart, self.ui.dateTimeEnd)
        self.ui.lineChart = LineChart(self.ui.lineChartPage, self.emotionData.data)
        self.ui.scatterPlot = ScatterPlot(self.ui.scatterPlotPage, self.emotionData.data)
        self.ui.pieChart = PieChart(self.ui.pieChartPage, self.emotionData.data)
        self.ui.barChart = BarChart(self.ui.barChartPage, self.emotionData.data)

        # Refresh data when refresh button clicked
        self.ui.refreshBtn.clicked.connect(self.refresh_data)

    def refresh_data(self):
        self.ui.dateTimeEnd.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeStart.setDateTime(QDateTime.currentDateTime().addDays(-1))
        self.update_data()

    def update_data(self, *args):
        self.emotionData.refresh_data(self.ui.dateTimeStart, self.ui.dateTimeEnd)
        self.ui.lineChart.update_data(self.emotionData.data)
        self.ui.scatterPlot.update_data(self.emotionData.data)
        self.ui.pieChart.update_data(self.emotionData.data)
        self.ui.barChart.update_data(self.emotionData.data)

    def start_service(self, checked):
        if checked and self.status != win32service.SERVICE_RUNNING:
            win32serviceutil.StartService(self.service_name, args=("",))
        elif not checked and self.status == win32service.SERVICE_RUNNING:
            win32serviceutil.StopService(self.service_name)

    def get_auto_start(self):
        return (
            win32serviceutil.QueryServiceConfig(self.service_name)[1]["start_type"]
            == win32service.SERVICE_AUTO_START
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
