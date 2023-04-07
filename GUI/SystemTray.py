
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QWidget, QHBoxLayout, QLabel, QComboBox, QCheckBox, QMessageBox
from PyQt5.QtGui import QIcon
import sys


class SystemTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(
                None,
                "Systray",
                "I couldn't detect any system tray on this system.",
            )
            sys.exit(1)
        super().__init__(parent)
        self.parent = parent
        self.setIcon(QIcon("public/logo.png"))
        

        self.setToolTip("FaceWatch")

        menu = QMenu()
        self.action_hide = QAction("Hide Window")
        menu.addAction(self.action_hide)

        self.labeling_action = QAction("Labeling Emotions")
        menu.addAction(self.labeling_action)

        self.action_show = QAction("Show Window")
        menu.addAction(self.action_show)

        self.action_exit = QAction("Exit")
        menu.addAction(self.action_exit)

        self.action_exit.triggered.connect(sys.exit)

        self.setContextMenu(menu)




