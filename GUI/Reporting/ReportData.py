from DB.Data import Data
from PyQt5.QtWidgets import QWidget, QLabel, QListWidgetItem, QHBoxLayout


class ReportData:
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget
        self.data = Data.get_instant()
        self.report = None
        self.report_data = None
        self.show_reports()

    def show_reports(self):
        self.report_data = self.data.get_all_reports()
        self.parent_widget.clear()
        for row in self.report_data:
            parent_widget = QWidget()
            layout = QHBoxLayout(parent_widget)
            label = QLabel(parent_widget)
            label.setWordWrap(True)
            label.setText(row[1])
            layout.addWidget(label)
            parent_widget.setStyleSheet(
                "QLabel, QListWidgetItem {font-size:20px; background-color : black; color : white; width:100%; border-radius: 20px; padding: 50px; }"
            )
            item = QListWidgetItem(self.parent_widget)
            item.setSizeHint(parent_widget.sizeHint())
            self.parent_widget.addItem(item)
            self.parent_widget.setItemWidget(item, parent_widget)
            # self.parent_widget.itemClicked.connect(self.show_report)
