import sys
from PySide2 import *
from ui_interface import Ui_MainWindow
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from DataAnalysis.LineChart import LineChart
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
from Background.DownloadModelsTask import DownloadModelsTask
from chatbot.Open_AI import *

# from register import *
import tkinter as tk
import requests


from constants import dir_name
print(dir_name)

import subprocess
class FirstWindow(QMainWindow):
    registration_successful = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("registeration")
        self.setGeometry(100, 100, 400, 200)
       
        # Username label and input field
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        # Password label and input field
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

            # Email label and input field for signup
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()

            # Password confirmation label and input field for signup
        self.confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

            # Signup button
        self.signup_button = QPushButton("Signup")
        self.signup_button.clicked.connect(self.signup)

            # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

            # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.login_button)

            # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def signup(self):
        # Get signup data from input fields
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        confirm_password = self.confirm_password_input.text()
        user = json={"username": username, "password": password, "email": email, "confirm_password": confirm_password}
        # user.save()
        # response = requests.post("http://127.0.0.1:8000/authentication/api/signup/", json={"username": username, "password": password, "email": email, "confirm_password":confirm_password})
        response = requests.post("http://127.0.0.1:8000/authentication/api/signup/", user)
        if response.ok and password == confirm_password:
            print("Registration successful!")
            self.registration_successful.emit()
            self.open_main_window()        
        else:
            print("Registration failed.")

        self.clear_input_fields()

    def login(self):
        # Get login data from input fields
        username = self.username_input.text()
        password = self.password_input.text()
        user = json={"username": username, "password": password}
        response = requests.post("http://127.0.0.1:8000/authentication/api/login/", user)
        if response.ok:
            print("Login successful!")
            self.registration_successful.emit()
            self.open_main_window()        # Launch main application
        else:
            print("Login failed.")
        self.clear_input_fields()

    def open_main_window(self):
        # Close the signup/login window
        self.close()

        # Open the main window
        main_window = MainWindow()
        main_window.show()

    def clear_input_fields(self):
        # Clear all input fields
        self.username_input.clear()
        self.password_input.clear()
        self.email_input.clear()
        self.confirm_password_input.clear()
        
# class ChatWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("ChatBot Window")
#         self.setGeometry(100, 100, 400, 200)

#         self.chat_bot = ChatBot()  # Create an instance of the ChatBot
#         self.layout = QVBoxLayout(self)

#         self.text_edit = QTextEdit()
#         self.text_edit.setReadOnly(True)
#         self.layout.addWidget(self.text_edit)

#         self.input_line = QLineEdit()
#         self.send_button = QPushButton("Send")
#         self.send_button.clicked.connect(self.send_message)
        
#         input_layout = QHBoxLayout()
#         input_layout.addWidget(self.input_line)
#         input_layout.addWidget(self.send_button)
#         self.layout.addLayout(input_layout)

#         self.chat_bot.message_received.connect(self.update_text)

#     def update_text(self, text):
#         self.text_edit.append(text)

#     def send_message(self):
#         message = self.input_line.text()
#         if message:
#             self.text_edit.append("You: " + message)
#             self.chat_bot.send_message(message)
#             self.input_line.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        self.service_name = "FaceWatchService"
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        loadJsonStyle(self, self.ui)
        self.show()

        # self.chat_window = ChatWindow()
        # self.chat_window.show()
        # self.ui.chatButton.clicked.connect(self.chat_window.show)
        # def __init__(self):
        #     super().__init__()
        #     self.setWindowTitle("ChatBot App")
        
        #     self.chat_bot = ChatBot()  # Create an instance of the ChatBot
        
        #     self.central_widget = QWidget()
        #     self.setCentralWidget(self.central_widget)
        
        #     self.layout = QVBoxLayout(self.central_widget)
        
        #     self.chat_button = QPushButton("Open Chat")
        #     self.chat_button.clicked.connect(self.open_chat)
        
        #     self.layout.addWidget(self.chat_button)
        
        # def open_chat(self):
        #     self.chat_window.show()

        # self.centralwidget = QtWidgets.QWidget()
        # self.centralwidget.setObjectName("centralwidget")
        # self.setCentralWidget(self.centralwidget)

        # self.chatButton = QtWidgets.QPushButton(self.centralwidget)
        # self.chatButton.setGeometry(QtCore.QRect(10, 10, 100, 50))
        # self.chatButton.setObjectName("chatButton")
        # self.chatButton.setText("Chat") 
        # #chat part
        # # self.ui.chatButton.clicked.connect(self.open_chat)\
        # self.openai_chat = ChatBot()
        # self.chatButton.clicked.connect(self.openai_chat.open_chat)

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

        # downloading models from github
        self.download_models_task = DownloadModelsTask()
        self.download_models_task.finished.connect(
            lambda: print("download models finished")
        )
        self.download_models_task.started.connect(
            lambda: print("download models started")
        )
        self.download_models_task.start_task()

        # generate report
        self.ui.getNewReport.clicked.connect(self.generate_report)

        # handle navigation
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.leftStackWidget.setCurrentWidget(self.ui.page))
        self.ui.infoBtn.clicked.connect(lambda: self.ui.leftStackWidget.setCurrentWidget(self.ui.page_2))
        self.ui.helpBtn.clicked.connect(lambda: self.ui.leftStackWidget.setCurrentWidget(self.ui.page_3))
        self.ui.homeBtn.clicked.connect(lambda: self.ui.centerMenuPages.setCurrentWidget(self.ui.page_4))
        self.ui.dataBtn.clicked.connect(lambda: self.ui.centerMenuPages.setCurrentWidget(self.ui.page_5))
        self.ui.reportsBtn.clicked.connect(lambda: self.ui.centerMenuPages.setCurrentWidget(self.ui.page_6))
        self.ui.snapHealthBtn.clicked.connect(lambda: self.ui.centerMenuPages.setCurrentWidget(self.ui.page_7))
        self.ui.barChartBtn.clicked.connect(lambda: self.ui.dataAnalysisPages.setCurrentWidget(self.ui.barChartPage))
        self.ui.pieChartBtn.clicked.connect(lambda: self.ui.dataAnalysisPages.setCurrentWidget(self.ui.pieChartPage))
        self.ui.lineChartBtn.clicked.connect(lambda: self.ui.dataAnalysisPages.setCurrentWidget(self.ui.lineChartPage))
        


        
    def generate_report(self):
        self.ui.getNewReport.setEnabled(False)
        self.ui.getNewReport.setText("Generating...")
        QApplication.processEvents()

        self.reportData.add_report()
        self.ui.getNewReport.setText("Generate Report")
        self.ui.getNewReport.setEnabled(True)
        QMessageBox.information(None, "Success", "Report generated successfully")

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
    window = MainWindow()
    window.show()
    window.ui.rightMenuContainer.expandMenu()
    window.ui.snapHealthBtn.click()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # TODO: fix this
    # \app.setQuitOnLastWin
    # dowClosed(False)
    # tray icon

    tray = SystemTray(parent=app)
    tray.show()

    registerwindow = FirstWindow()
    def show_window():
        window = MainWindow()
        window.show()

    # registerwindow.show()

    registerwindow.registration_successful.connect(show_window)
    app.lastWindowClosed.connect(app.quit)

    tray.action_hide.triggered.connect(registerwindow.hide)
    tray.action_show.triggered.connect(registerwindow.show)
    tray.labeling_action.triggered.connect(handle_labeling_action)
    registerwindow.show()
    sys.exit(app.exec_())
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = FirstWindow()
#     window.show()
#     sys.exit(app.exec_())
