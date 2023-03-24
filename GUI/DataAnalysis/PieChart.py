from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtWidgets import QVBoxLayout

class PieChart(QChartView):
    def __init__(self, parent_widget, data):
        self.series = QPieSeries()
        emotions = {"angry": 0, "disgust": 0, "fear": 0, "happy": 0, "sad": 0, "surprise": 0, "neutral": 0}
        for item in data:
            emotions[item[1]] += 1
        for emotion, count in emotions.items():
            self.series.append(emotion, count)
        self.series.setLabelsVisible(True)
        self.series.setLabelsPosition(QPieSlice.LabelInsideHorizontal)
        self.series.setPieSize(1)
        self.series.setPieStartAngle(0)
        self.series.setPieEndAngle(360)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Pie Chart Showing Emotions Distribution")
        self.chart.legend().setAlignment(Qt.AlignRight)
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        parent_widget.setLayout(self.layout)
    
    def update_data(self, new_data):
        self.series.clear()
        emotions = {"angry": 0, "disgust": 0, "fear": 0, "happy": 0, "sad": 0, "surprise": 0, "neutral": 0}
        for item in new_data:
            emotions[item[1]] += 1
        for emotion, count in emotions.items():
            self.series.append(emotion, count)
        self.series.setLabelsVisible(True)
        self.series.setLabelsPosition(QPieSlice.LabelInsideHorizontal)
        self.series.setPieSize(1)
        self.series.setPieStartAngle(0)
        self.series.setPieEndAngle(360)
