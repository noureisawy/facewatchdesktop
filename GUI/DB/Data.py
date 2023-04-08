import sqlite3
from PyQt5.QtWidgets import QMessageBox

db_path = "C:/Users/UG/Desktop/research/FaceWatch/GUI/DB/emotions.db"


class Data:
    __data = None
    
    @classmethod
    def get_instant(cls):
        if cls.__data is None:
            cls.__data = Data()
        return cls.__data

    def __init__(self):
        if Data.__data is not None:
            raise Exception("This class is a singleton!")
        self.conn = None
        self.create_database_and_connect()

    def create_database_and_connect(self):
        try:
            # Connect to the database or create it if it doesn't exist
            self.conn = sqlite3.connect(db_path)

            # Create a table to store emotions if it doesn't exist
            self.create_emotions_table()
            # Create a table to store tiredness if it doesn't exist
            self.create_tiredness_table()
            # Create a table to user information if it doesn't exist
            self.create_user_information_table()

        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while connecting to the database: {e}",
            )

    def create_table(self, arg0):
        cursor = self.conn.cursor()
        cursor.execute(arg0)
        self.conn.commit()

    def create_tiredness_table(self):
        try:
            self.create_table(
                """
            CREATE TABLE IF NOT EXISTS tiredness (
                id INTEGER PRIMARY KEY,
                tiredness TEXT NOT NULL,
                timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
            )
            """
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the tiredness table: {e}",
            )

    def create_user_information_table(self):
        # Create a table to store user information if it doesn't exist, birth year, gender, medical history
        try:
            self.create_table(
                """
                CREATE TABLE IF NOT EXISTS user_information (
                    id INTEGER PRIMARY KEY,
                    birth_year INTEGER,
                    gender TEXT,
                    current_emotion TEXT,
                    alertness_state TEXT,
                    current_mental_health TEXT,
                    medical_history TEXT,
                    current_symptoms_concerns TEXT,
                    created_at DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
                )
                    """
            )
            # create first user information
            self.create_user_information()

        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the user information table: {e}",
            )

    def create_emotions_table(self):
        try:
            self.create_table(
                """
            CREATE TABLE IF NOT EXISTS emotions (
                id INTEGER PRIMARY KEY,
                emotion TEXT NOT NULL,
                angry INTEGER NOT NULL,
                disgust INTEGER NOT NULL,
                fear INTEGER NOT NULL,
                happy INTEGER NOT NULL,
                sad INTEGER NOT NULL,
                surprise INTEGER NOT NULL,
                neutral INTEGER NOT NULL, 
                timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
            )
            """
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the emotions table: {e}",
            )

    def get_user_information(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM user_information
                """
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while retrieving user information: {e}",
            )

    def get_date_between(self, start_date, end_date, table_name="emotions"):
        if table_name == "emotions":
            try:
                return self._extracted_from_get_date_between_4(
                    """
                SELECT * FROM emotions WHERE timestamp BETWEEN ? AND ?
                """,
                    start_date,
                    end_date,
                )
            except sqlite3.Error as e:
                print(e)
                QMessageBox.critical(
                    None, "Error", f"An error occurred while retrieving data: {e}"
                )
        elif table_name == "tiredness":
            try:
                return self._extracted_from_get_date_between_4(
                    """
                SELECT * FROM tiredness WHERE timestamp BETWEEN ? AND ?
                """,
                    start_date,
                    end_date,
                )
            except sqlite3.Error as e:
                print(e)
                QMessageBox.critical(
                    None, "Error", f"An error occurred while retrieving data: {e}"
                )

    def _extracted_from_get_date_between_4(self, arg0, start_date, end_date):
        cursor = self.conn.cursor()
        cursor.execute(arg0, (start_date, end_date))
        return cursor.fetchall()

    def delete_between(self, start_date, end_date, table_name="emotions"):
        if table_name == "emotions":
            try:
                self._extracted_from_delete_between_4(
                    """
                DELETE FROM emotions WHERE timestamp BETWEEN ? AND ?
                """,
                    start_date,
                    end_date,
                )
            except sqlite3.Error as e:
                print(e)
                QMessageBox.critical(
                    None, "Error", f"An error occurred while deleting data: {e}"
                )
        elif table_name == "tiredness":
            try:
                self._extracted_from_delete_between_4(
                    """
                DELETE FROM tiredness WHERE timestamp BETWEEN ? AND ?
                """,
                    start_date,
                    end_date,
                )
            except sqlite3.Error as e:
                print(e)
                QMessageBox.critical(
                    None, "Error", f"An error occurred while deleting data: {e}"
                )

    def _extracted_from_delete_between_4(self, arg0, start_date, end_date):
        cursor = self.conn.cursor()
        cursor.execute(arg0, (start_date, end_date))
        self.conn.commit()

    def insert_tiredness(self, tiredness):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO tiredness (tiredness) VALUES (?)
                """,
                (tiredness,),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None, "Error", f"An error occurred while inserting data: {e}"
            )

    def update_user_information(
        self,
        birth_year=None,
        gender=None,
        medical_history=None,
        current_emotion=None,
        alertness_state=None,
        current_mental_health=None,
        current_symptoms_concerns=None,
    ):
        # update user information
        try:
            cursor = self.conn.cursor()
            if birth_year:
                cursor.execute(
                    """
                    UPDATE user_information SET birth_year = ? WHERE id = 1
                    """,
                    (birth_year,),
                )
            if gender:
                cursor.execute(
                    """
                    UPDATE user_information SET gender = ? WHERE id = 1
                    """,
                    (gender,),
                )
            if medical_history:
                cursor.execute(
                    """
                    UPDATE user_information SET medical_history = ? WHERE id = 1
                    """,
                    (medical_history,),
                )
            if current_emotion:
                cursor.execute(
                    """
                    UPDATE user_information SET current_emotion = ? WHERE id = 1
                    """,
                    (current_emotion,),
                )
            if alertness_state:
                cursor.execute(
                    """
                    UPDATE user_information SET alertness_state = ? WHERE id = 1
                    """,
                    (alertness_state,),
                )
            if current_mental_health:
                cursor.execute(
                    """
                    UPDATE user_information SET current_mental_health = ? WHERE id = 1
                    """,
                    (current_mental_health,),
                )
            if current_symptoms_concerns:
                cursor.execute(
                    """
                    UPDATE user_information SET current_symptoms_concerns = ? WHERE id = 1
                    """,
                    (current_symptoms_concerns,),
                )
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while updating user information: {e}",
            )

    def create_user_information(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO user_information (id) VALUES (1)
                """
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting user information: {e}",
            )

    def insert_emotion(self, emotion_json_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
            INSERT INTO emotions (emotion, angry, disgust, fear, happy, sad, surprise, neutral) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    emotion_json_data["dominant_emotion"],
                    emotion_json_data["emotion"]["angry"],
                    emotion_json_data["emotion"]["disgust"],
                    emotion_json_data["emotion"]["fear"],
                    emotion_json_data["emotion"]["happy"],
                    emotion_json_data["emotion"]["sad"],
                    emotion_json_data["emotion"]["surprise"],
                    emotion_json_data["emotion"]["neutral"],
                ),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None, "Error", f"An error occurred while inserting data: {e}"
            )
