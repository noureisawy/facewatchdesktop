
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QWidget, QHBoxLayout, QLabel, QComboBox, QCheckBox, QMessageBox
from PyQt5.QtGui import QIcon
import sys


class SystemTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(self)
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(
                None,
                "Systray",
                "I couldn't detect any system tray on this system.",
            )
            sys.exit(1)
        self.parent = parent
        self.setIcon(QIcon("public/logo.png"))
        self.setToolTip("FaceWatch")
        self.activated.connect(self.onTrayIconActivated)

        menu = QMenu()

        action_hide = QAction("Hide Window")
        menu.addAction(action_hide)
        action_hide.triggered.connect(self.parent.hide)

        action_show = QAction("Show Window")
        menu.addAction(action_show)
        action_show.triggered.connect(self.parent.show)

        action_exit = QAction("Exit")
        action_exit.triggered.connect(sys.exit)
        menu.addAction(action_exit)
        self.setContextMenu(self.menu)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.parent.isVisible():
                self.parent.hide()
            else:
                self.parent.show()


