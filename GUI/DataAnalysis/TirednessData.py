from DB.Data import Data
from PyQt5.QtChart import QLineSeries
from PyQt5.QtCore import QDateTime


class TirednessData:
    def __init__(self, dateTimeStartComponent, dateTimeEndComponent):
        self.type = "Tiredness"
        self.conn = Data()
        self.dateTimeStart = dateTimeStartComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.dateTimeEnd = dateTimeEndComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.dateTimeStartComponent = dateTimeStartComponent
        self.dateTimeEndComponent = dateTimeEndComponent
        self.data = self.conn.get_date_between(
            self.dateTimeStart, self.dateTimeEnd, table_name="tiredness"
        )

    def refresh_data(self, dateTimeStartComponent, dateTimeEndComponent):
        self.dateTimeStart = dateTimeStartComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.dateTimeEnd = dateTimeEndComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.data = self.conn.get_date_between(
            self.dateTimeStart, self.dateTimeEnd, table_name="tiredness"
        )

    def get_bar_chart_data(self):
        return self._extracted_from_get_bie_chart_data_2()

    def get_pie_chart_data(self):
        return self._extracted_from_get_bie_chart_data_2()

    def get_scatter_plot_data(self):
        return self._extracted_from_get_line_chart_data_2()

    def get_line_chart_data(self):
        return self._extracted_from_get_line_chart_data_2()

    # TODO Rename this here and in `get_bar_chart_data` and `get_bie_chart_data`
    def _extracted_from_get_bie_chart_data_2(self):
        tiredness = {
            "alert": 0,
            "non_vigilant": 0,
            "tired": 0,
        }
        for item in self.data:
            tiredness[item[1]] += 1
        return tiredness

    # TODO Rename this here and in `get_scatter_plot_data` and `get_line_chart_data`
    def _extracted_from_get_line_chart_data_2(self):
        x = [QDateTime.fromString(item[9], "yyyy-MM-dd HH:mm:ss") for item in self.data]
        y = [item[1] for item in self.data]
        tiredness = {
            "alert": 1,
            "non_vigilant": 2,
            "tired": 3,
        }
        y_numeric = [tiredness[i] for i in y]
        labels = tiredness
        return x, y_numeric, labels
