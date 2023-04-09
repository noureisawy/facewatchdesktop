from DB.Data import Data
from ui_dataRow import Ui_Form
from PyQt5.QtWidgets import (
    QListWidgetItem,
    QWidget,
    QDialogButtonBox,
    QDialog,
    QVBoxLayout,
    QLineEdit,
)
from EmotionGallery.ReadImages import ReadLabeledImage
import functools


class LabelingData:
    def __init__(self, widget, image_container, lower_widget):
        self.widget = widget
        self.data = Data.get_instant()
        self.label = None
        self.lower_widget = lower_widget
        self.image_container = image_container
        self.read_labeled_image = ReadLabeledImage(self.image_container)

    def set_label(self, label):
        self.label = label
        self.update_widget()

    def update_widget(self):
        data_dict = {
            "emotions": self.data.get_all_emotions_labeling,
            "alertness": self.data.get_all_tiredness_labeling,
            "mental_health": self.data.get_all_mental_health_labeling,
            "symptoms": self.data.get_all_symptoms_concerns_labeling,
        }
        data = data_dict[self.label]()
        self.widget.clear()
        for row in data:
            print(row)
            parent_widget = QWidget()
            data_row = Ui_Form()
            data_row.setupUi(parent_widget)
            data_row.label.setText(row[2])
            data_row.label_2.setText(row[1])
            data_row.showImage.clicked.connect(
                functools.partial(self.show_image, created_at=row[2])
            )
            data_row.editLabel.clicked.connect(
                functools.partial(self.edit_label, data_row)
            )
            item = QListWidgetItem(self.widget)
            item.setSizeHint(parent_widget.sizeHint())
            self.widget.addItem(item)
            self.widget.setItemWidget(item, parent_widget)

    def show_image(self, created_at):
        print(created_at)
        self.read_labeled_image.set_attr(f"{self.label}_label", created_at)
        self.lower_widget.expandMenu()

    def edit_label(self, data_row):
        data_update = {
            "emotions": self.data.update_emotion_label,
            "alertness": self.data.update_tiredness_label,
            "mental_health": self.data.update_mental_health_label,
            "symptoms": self.data.update_symptoms_concerns_label,
        }
        print(self.label)
        update = data_update[self.label]
        # Create a dialog window
        dialog = QDialog()
        dialog.setWindowTitle("Edit Label")
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        # Add a line edit to the dialog window
        line_edit = QLineEdit()
        line_edit.setText(data_row.label_2.text())
        layout.addWidget(line_edit)

        # Add an OK button to the dialog window
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        # Show the dialog window and wait for the user to close it
        if dialog.exec_() == QDialog.Accepted:
            # Update the label text in the main window
            print(line_edit.text())
            print(data_row.label.text())
            data_row.label_2.setText(line_edit.text())
            update(line_edit.text(),data_row.label.text())
            
