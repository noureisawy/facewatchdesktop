
from PyQt5.QtChart import QChart, QChartView, QDateTimeAxis, QValueAxis, QLineSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QVBoxLayout
class LineChart(QChartView):
    def __init__(self, parent_widget, data):        
        self.series = data
        self.chart = QChart()
        x = [QDateTime.fromString(item[9], "yyyy-MM-dd HH:mm:ss") for item in data]
        y = [item[1] for item in data]
        # convert emotions to numerical values
        emotions = {"angry":1, "disgust":2, "fear":3, "happy":4, "sad":5, "surprise":6, "neutral":7}
        y = [emotions[i] for i in y]
        x_axis = QDateTimeAxis()
        x_axis.setTickCount(len(x))
        x_axis.setFormat('dd HH:mm:ss')
        x_axis.setRange(x[0], x[-1])
        x_axis.setLabelsAngle(-45)
        self.chart.addAxis(x_axis, Qt.AlignBottom)
        y_axis = QValueAxis()
        y_axis.setTickCount(len(emotions))
        y_axis.setRange(1, len(emotions))
        y_axis.setLabelFormat('%d')
        y_axis.setLabelsVisible(True)
        self.chart.addAxis(y_axis, Qt.AlignLeft)
        self.series = QLineSeries()
        for i in range(len(x)):
            print(x[i].toMSecsSinceEpoch())
            self.series.append(x[i].toMSecsSinceEpoch(), y[i])
        self.chart.addSeries(self.series)
        self.series.attachAxis(x_axis)
        self.series.attachAxis(y_axis)
        self.chart.setTitle("Line Chart Showing Emotions Over Time")
        self.chart.axisX().setTitleText("Time")
        self.chart.axisY().setTitleText("Emotions")
        self.chart.legend().hide()
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        parent_widget.setLayout(self.layout)


