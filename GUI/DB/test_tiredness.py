from Data import Data


data = Data.get_instant()
# insert some emotional data
data.insert_tiredness(
    "alert"
)
data.insert_tiredness(
    "non_vigilant"
)
data.insert_tiredness(
    "tired"
)

# get all data
print(data.get_date_between("2023-03-23 02:18:54", "2023-04-24 02:18:54", table_name="tiredness"))
