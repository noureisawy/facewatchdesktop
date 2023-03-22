from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QValueAxis, QBarCategoryAxis
from PyQt5.QtWidgets import QVBoxLayout

class BarChart(QChartView):
    def __init__(self, parent_widget):
        self.series = QBarSeries()
        self.set0 = QBarSet("Jane")
        self.set1 = QBarSet("Joe")
        self.set2 = QBarSet("Andy")
        self.set3 = QBarSet("Barbara")
        self.set4 = QBarSet("Axel")
        self.set0.append([1])
        self.set1.append([2])
        self.set2.append([3])
        self.set3.append([4])
        self.set4.append([5])
        self.series.append(self.set0)
        self.series.append(self.set1)
        self.series.append(self.set2)
        self.series.append(self.set3)
        self.series.append(self.set4)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Simple barchart example")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.axis = QBarCategoryAxis()
        self.axis.append([""])
        self.chart.createDefaultAxes()
        self.chart.setAxisX(self.axis, self.series)
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        parent_widget.setLayout(self.layout)


