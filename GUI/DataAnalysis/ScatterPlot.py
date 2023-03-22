
from PyQt5.QtChart import QChart, QChartView, QScatterSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout


class ScatterPlot(QChartView):

    def __init__(self, parent_widget):
        self.series = QScatterSeries()
        self.series.append(1, 2)
        self.series.append(2, 4)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("My Scatter Chart")
        self.chart.createDefaultAxes()
        self.chart.axisX().setTitleText("X Axis")
        self.chart.axisY().setTitleText("Y Axis")
        self.chart.legend().hide()
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        parent_widget.setLayout(self.layout)






