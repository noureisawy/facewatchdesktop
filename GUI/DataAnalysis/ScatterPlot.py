from PyQt5.QtChart import QChart, QChartView, QDateTimeAxis, QCategoryAxis, QScatterSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QVBoxLayout

class ScatterPlot(QChartView):
    def __init__(self, parent_widget, data):
        self.series = QScatterSeries()
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.legend().hide()
        axisX = QDateTimeAxis()
        axisX.setFormat("dd/MM/yyyy hh:mm:ss")
        axisX.setTitleText("Date")
        axisY = QCategoryAxis()
        axisY.setTitleText("Emotion")
        self.chart.setAxisX(axisX, self.series)
        self.chart.setAxisY(axisY, self.series)
        self.set_data(data)
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        self.series.setMarkerSize(20)
        parent_widget.setLayout(self.layout)

    def set_data(self, data):
        self.series.clear()
        self.chart.setTitle(f'Scatter Plot Showing {data.type} Over Time')
        x, y_numeric, labels = data.get_scatter_plot_data()
        for i in range(len(x)):
            self.series.append(x[i].toMSecsSinceEpoch(), y_numeric[i])
        if x:
            self.set_axisX_data(x)
        self.chart.axisY().setTickCount(len(labels))
        self.chart.axisY().setRange(0, len(labels)+1)
        self.chart.axisY().setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        self.chart.axisY().setLabelsFont(self.chart.font())
        for item, value in labels.items():
            self.chart.axisY().append(item, value)
        self.chart.axisX().setTitleText("Time")
        self.chart.axisY().setTitleText(f"{data.type}")
    
    def set_axisX_data(self, x):
        self.chart.axisX().setRange(x[0], x[-1])
        self.chart.axisX().setTickCount(len(x))
        self.chart.axisX().setTickCount(len(x))
        self.chart.axisX().setFormat('dd HH:mm:ss')
        self.chart.axisX().setRange(x[0], x[-1])
        self.chart.axisX().setLabelsAngle(-45)
