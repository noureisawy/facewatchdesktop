from DB.Data import Data
from PyQt5.QtChart import QLineSeries
from PyQt5.QtCore import QDateTime

class EmotionData:
    def __init__(self,dateTimeStartComponent, dateTimeEndComponent):
        self.type = "Emotions"
        self.conn = Data()
        self.dateTimeStart = dateTimeStartComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.dateTimeEnd = dateTimeEndComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.dateTimeStartComponent = dateTimeStartComponent
        self.dateTimeEndComponent = dateTimeEndComponent
        self.data = None
        # self.data = self.conn.get_date_between(self.dateTimeStart, self.dateTimeEnd)
    
    def refresh_data(self, dateTimeStartComponent, dateTimeEndComponent):
        self.dateTimeStart = dateTimeStartComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.dateTimeEnd = dateTimeEndComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.data = self.conn.get_date_between(self.dateTimeStart, self.dateTimeEnd)
    
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
        emotions = {
            "angry": 0,
            "disgust": 0,
            "fear": 0,
            "happy": 0,
            "sad": 0,
            "surprise": 0,
            "neutral": 0,
        }
        if self.data is None:
            self.data = self.conn.get_date_between(self.dateTimeStart, self.dateTimeEnd)
        for item in self.data:
            emotions[item[1]] += 1
        return emotions
    
    # TODO Rename this here and in `get_scatter_plot_data` and `get_line_chart_data`
    def _extracted_from_get_line_chart_data_2(self):
        if self.data is None:
            self.data = self.conn.get_date_between(self.dateTimeStart, self.dateTimeEnd)

        x = [
            QDateTime.fromString(item[9], "yyyy-MM-dd HH:mm:ss")
            for item in self.data
        ]
        y = [item[1] for item in self.data]
        emotions = {
            "angry": 1,
            "disgust": 2,
            "fear": 3,
            "happy": 4,
            "sad": 5,
            "surprise": 6,
            "neutral": 7,
        }
        y_numeric = [emotions[i] for i in y]
        labels = emotions
        return x, y_numeric, labels

    
