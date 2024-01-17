import os
from datetime import datetime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from DB.Data import Data
import os

project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

project_path = project_path.replace("\\", "/")
directory = project_path + "/Images"


class ReadImages:
    def __init__(self, dir, list_widget):
        self.directory = dir
        self.images = []
        self.read_images()
        self.list_widget = list_widget
        self.show_image()

    def refresh(self, new_directory):
        self.directory = new_directory
        self.images = []
        self.read_images()
        self.show_image()

    def show_image(self):
        self.list_widget.clear()
        horizontal_layout = QHBoxLayout()
        outer_widget = QWidget()
        # delete images if there are more than 50
        if len(self.images) > 50:
            for image in self.images[50:]:
                os.remove(image)
            self.images = self.images[:50]

        for image in self.images:
            filename = image.split("/")[-1].split(".")[0]
            filename = datetime.strptime(filename, "%Y%m%d-%H%M%S")
            label_text = QLabel(str(filename))
            label_text.setAlignment(Qt.AlignCenter)
            label = QLabel()
            label.setFixedSize(250, 250)
            label.setPixmap(QPixmap(image))
            label.setScaledContents(True)
            widget = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(label_text)
            widget.setLayout(layout)
            horizontal_layout.addWidget(widget)
        outer_widget.setLayout(horizontal_layout)
        list_item = QListWidgetItem()
        list_item.setSizeHint(outer_widget.sizeHint())
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, outer_widget)

    def read_images(self):
        for filename in os.listdir(f"{directory}/{self.directory}"):
            if filename.endswith(".jpg"):
                self.images.append(f"{directory}/{self.directory}/{filename}")
        return self.images.reverse()


class ReadLabeledImage(ReadImages):
    def __init__(self, list_widget):
        self.date_created = None
        super().__init__("", list_widget)

    def set_attr(self, label, date_created):
        self.date_created = date_created
        self.directory = label
        self.refresh()

    def read_images(self):
        if self.date_created is None:
            return []
        file_name = f"{directory}/{self.directory}/{self.date_created}.jpg"
        print(file_name)
        if os.path.exists(file_name):
            self.images.append(file_name)
        return self.images

    def refresh(self):
        self.images = []
        self.read_images()
        self.show_image()
