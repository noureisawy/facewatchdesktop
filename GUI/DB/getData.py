
from Data import Data

data = Data.get_instant()

print(data.get_date_between("2021-03-23 14:47:00", "2023-04-23 14:49:00")[0][0])

data.delete_between("2021-03-21 14:47:00", "2023-04-23 14:49:00")
