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
        self.series = QBarSeries()
        self.chart = QChart()
        # self.set_data(data)
        self.chart.addSeries(self.series)
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
    
    def set_data(self, data):
        self.series.clear()
        data_ptl = data.get_bar_chart_data()
        for item, count in data_ptl.items():
            set0 = QBarSet(item)
            set0.append(count)
            self.series.append(set0)
        self.chart.setTitle(f'Bar Chart Showing {data.type} Over Time')