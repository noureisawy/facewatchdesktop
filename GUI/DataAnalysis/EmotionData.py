from DB.Data import Data
from PyQt5.QtChart import QLineSeries

class EmotionData:
    def __init__(self,dateTimeStartComponent, dateTimeEndComponent):
        self.conn = Data()
        self.dateTimeStart = dateTimeStartComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.dateTimeEnd = dateTimeEndComponent.dateTime().toString(
            "yyyy-MM-dd hh:mm:ss"
        )
        self.dateTimeStartComponent = dateTimeStartComponent
        self.dateTimeEndComponent = dateTimeEndComponent
        self.data = self.conn.get_date_between(self.dateTimeStart, self.dateTimeEnd)
    

    
