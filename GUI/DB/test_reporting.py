
from Data import Data

data = Data.get_instant()

data.insert_report("first text for report")
data.insert_report("second text for report")
data.insert_report("third text for report")
data.insert_report("fourth text for report")
data.insert_report("fifth text for report")
data.insert_report("sixth text for report")
data.insert_report("seventh text for report")
data.insert_report("eighth text for report")

print(data.get_all_reporting_data())
print("done")
