from PyQt5.QtChart import QChart, QChartView, QDateTimeAxis, QCategoryAxis, QLineSeries
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
        self.emotions = {"angry":1, "disgust":2, "fear":3, "happy":4, "sad":5, "surprise":6, "neutral":7}
        y_numeric = [self.emotions[i] for i in y]
        # create category axis for self.emotions
        y_axis = QCategoryAxis()
        y_axis.setTickCount(len(self.emotions))
        y_axis.setRange(0, len(self.emotions)+1)
        y_axis.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        y_axis.setLabelsFont(self.chart.font())
        for emotion, value in self.emotions.items():
            y_axis.append(emotion, value)
        self.chart.addAxis(y_axis, Qt.AlignLeft)
        self.series = QLineSeries()
        for i in range(len(x)):
            self.series.append(x[i].toMSecsSinceEpoch(), y_numeric[i])
        self.chart.addSeries(self.series)
        x_axis = QDateTimeAxis()
        x_axis.setTickCount(len(x))
        x_axis.setFormat('dd HH:mm:ss')
        x_axis.setRange(x[0], x[-1])
        x_axis.setLabelsAngle(-45)
        self.series.attachAxis(x_axis)
        self.series.attachAxis(y_axis)
        self.chart.addAxis(x_axis, Qt.AlignBottom)
        self.chart.setTitle("Line Chart Showing Emotions Over Time")
        self.chart.axisX().setTitleText("Time")
        self.chart.axisY().setTitleText("Emotions")
        self.chart.legend().hide()
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        parent_widget.setLayout(self.layout)
    
    def update_data(self,new_data):
        self.series.clear()
        x = [QDateTime.fromString(item[9], "yyyy-MM-dd HH:mm:ss") for item in new_data]
        y = [item[1] for item in new_data]
        # convert emotions to numerical values
        y_numeric = [self.emotions[i] for i in y]
        for i in range(len(x)):
            self.series.append(x[i].toMSecsSinceEpoch(), y_numeric[i])
        if x:
            self.chart.axisX().setRange(x[0], x[-1])
            self.chart.axisX().setTickCount(len(x))
        


