from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtChart import (
    QChart,
    QChartView,
    QBarSet,
    QBarSeries,
    QValueAxis,
)
from PyQt5.QtWidgets import QVBoxLayout


class BarChart(QChartView):
    def __init__(self, parent_widget, data):
        self.emotions = {
            "angry": 0,
            "disgust": 0,
            "fear": 0,
            "happy": 0,
            "sad": 0,
            "surprise": 0,
            "neutral": 0,
        }
        for item in data:
            self.emotions[item[1]] += 1
        self.series = QBarSeries()
        for emotion, count in self.emotions.items():
            set0 = QBarSet(emotion)
            set0.append(count)
            self.series.append(set0)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Bar Chart Showing Emotions Distribution")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.axis = QValueAxis()
        self.axis.setLabelFormat("%i")
        self.chart.setAxisY(self.axis, self.series)
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        parent_widget.setLayout(self.layout)

    def update_data(self, new_data):
        self.series.clear()
        self.emotions = {
            "angry": 0,
            "disgust": 0,
            "fear": 0,
            "happy": 0,
            "sad": 0,
            "surprise": 0,
            "neutral": 0,
        }
        for item in new_data:
            self.emotions[item[1]] += 1
        for emotion, count in self.emotions.items():
            set0 = QBarSet(emotion)
            set0.append(count)
            self.series.append(set0)
