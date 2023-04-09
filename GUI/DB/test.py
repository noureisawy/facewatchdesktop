
from Data import Data

# delete user_information table

data = Data()
cursor = data.conn.cursor()
cursor.execute("DROP TABLE labeling_emotions")
cursor.execute("DROP TABLE labeling_tiredness")
cursor.execute("DROP TABLE labeling_symptoms_concerns")
cursor.execute("DROP TABLE labeling_mental_health")
data.conn.commit()


