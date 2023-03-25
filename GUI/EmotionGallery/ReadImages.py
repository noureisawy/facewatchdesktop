
import os
from datetime import datetime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
directory = "C:/Users/UG/Desktop/research/FaceWatch/Images"

class ReadImages:
    def __init__(self, emotion, list_widget):
        self.emotion = emotion
        self.images = []
        self.read_images()
        self.list_widget = list_widget
        self.show_image()
    
    def refresh(self, new_emotion):
        self.emotion = new_emotion 
        self.images = []
        self.read_images()
        self.show_image()

    def show_image(self):
        self.list_widget.clear()
        horizontal_layout = QHBoxLayout()
        outer_widget = QWidget()
        for image in self.images:
            filename = image.split("/")[-1].split(".")[0]
            filename = datetime.strptime(filename, "%Y%m%d-%H%M%S")
            label_text = QLabel(str(filename))
            label_text.setAlignment(Qt.AlignCenter)
            label = QLabel()
            label.setFixedSize(300, 300)
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
        for filename in os.listdir(f"{directory}/{self.emotion}"):
            if filename.endswith(".jpg"):
                self.images.append(f"{directory}/{self.emotion}/{filename}")
        return self.images.reverse()
    
            



