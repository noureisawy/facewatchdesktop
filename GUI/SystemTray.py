
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

        # Create a widget with a combo box and a counter
        widget = QWidget()
        layout = QHBoxLayout(widget)
        self.combo_box = QComboBox()
        self.combo_box.addItems(['Option 1', 'Option 2', 'Option 3'])
        layout.addWidget(self.combo_box)
        self.counter_label = QLabel('0')
        layout.addWidget(self.counter_label)


        self.setToolTip("FaceWatch")

        menu = QMenu()
        # add widget to the menu
        self.action_hide = QAction("Hide Window")
        menu.addAction(self.action_hide)

        self.action_show = QAction("Show Window")
        menu.addAction(self.action_show)

        self.action_exit = QAction("Exit")
        menu.addAction(self.action_exit)

        self.action_exit.triggered.connect(sys.exit)

        self.setContextMenu(menu)




