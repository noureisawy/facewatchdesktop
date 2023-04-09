
from DB.Data import Data
from ui_dataRow import Ui_DataRow

class LabelingData:

    def __init__(self, table_window):
        self.table_window = table_window 
        self.data = Data.get_instant()
        self.label = None

    def set_label(self, label):
        self.label = label
        self.update_table()

    def update_table(self):
        data_label = self.data.get_data_label(self.label)
        
        
    

    




