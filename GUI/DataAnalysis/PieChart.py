from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtWidgets import QVBoxLayout

class PieChart(QChartView):
    def __init__(self, parent_widget, data):
        self.series = QPieSeries()
        self.series.setLabelsVisible(True)
        self.series.setLabelsPosition(QPieSlice.LabelInsideHorizontal)
        self.series.setPieSize(1)
        self.series.setPieStartAngle(0)
        self.series.setPieEndAngle(360)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.legend().setAlignment(Qt.AlignRight)
        self.set_data(data)
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        parent_widget.setLayout(self.layout)
    
    def set_data(self, data):
        self.series.clear()
        data_plt = data.get_pie_chart_data()
        total_count = sum(data_plt.values())
        for item, count in data_plt.items():
            if total_count == 0:
                self.series.append(item, count)
            else:
                slice_ = QPieSlice(item, count)
                percentage = count / total_count * 100
                slice_.setLabel(f"{item} ({percentage:.1f}%)")
                self.series.append(slice_)
        self.chart.setTitle(f'Pie Chart Showing {data.type} Over Time')
