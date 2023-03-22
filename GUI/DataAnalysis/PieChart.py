from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtWidgets import QVBoxLayout

class PieChart(QChartView):

    def __init__(self, parent_widget):
        self.series = QPieSeries()
        self.series.append("Jane", 1)
        self.series.append("Joe", 2)
        self.series.append("Andy", 3)
        self.series.append("Barbara", 4)
        self.series.append("Axel", 5)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Simple piechart example")
        self.chart.legend().hide()
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        parent_widget.setLayout(self.layout)
