########################################################################
## IMPORTS
########################################################################
import sys
import os
from PySide2 import *


########################################################################
# IMPORT GUI FILE
from ui_interface import *

########################################################################

########################################################################
# IMPORT Custom widgets
from Custom_Widgets.Widgets import *

########################################################################
########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinndesign.com
########################################################################

########################################################################
## IMPORTS
########################################################################
import sys
import os
from PySide2 import *


########################################################################
# IMPORT GUI FILE
from ui_interface import *

########################################################################

########################################################################
# IMPORT Custom widgets
from Custom_Widgets.Widgets import *

########################################################################

import win32serviceutil

import servicemanager
import win32event
import win32service


########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        self.service_name = "FaceWatchService"
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        loadJsonStyle(self, self.ui)
        ########################################################################
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

    def start_service(self, checked):  # sourcery skip: avoid-builtin-shadow
        if checked and self.status != win32service.SERVICE_RUNNING:
            # Replace "service_name" with the name of your Windows service
            win32serviceutil.StartService(
                self.service_name, args=("",)
            )
        elif not checked:
            # Stop the service if the checkbox is unchecked
            win32serviceutil.StopService(self.service_name)

    def get_auto_start(self):
        return (
            win32serviceutil.QueryServiceConfig(self.service_name)[1]["start_type"]
            == win32service.SERVICE_AUTO_START
        )


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################
