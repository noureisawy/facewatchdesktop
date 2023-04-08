import sqlite3
from PyQt5.QtWidgets import QMessageBox

db_path = "C:/Users/UG/Desktop/research/FaceWatch/GUI/DB/emotions.db"

from datetime import datetime

class Data:
    __data = None

    @classmethod
    def get_instant(cls):
        if cls.__data is None:
            cls.__data = Data()
        return cls.__data

    def __init__(self):  # sourcery skip: raise-specific-error
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
            # Create a table to store labeling emotions associated with user face images
            self.create_labeling_emotions_table()
            # Create a table to store labeling tiredness associated with user face images
            self.create_labeling_tiredness_table()
            # Create a table to store labeling mental health associated with user face images
            self.create_labeling_mental_health()
            # Create a table to store labeling symptoms and concerns associated with user face images
            self.create_labeling_symptoms_concerns()


        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while connecting to the database: {e}",
            )


    def create_labeling_emotions_table(self):
        # create a table to store labeling emotions associated with user face images
        try:
            self.create_table(
                """
                CREATE TABLE IF NOT EXISTS labeling_emotions (
                    id INTEGER PRIMARY KEY,
                    emotion TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                    """
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the labeling emotions table: {e}",
            )
    
    def insert_into_emotion_labeling(self, emotion, image_path):
        # insert into labeling emotions table
        try:
            self.insert_into_table(
                """
                INSERT INTO labeling_emotions(emotion, image_path, created_at)
                VALUES(?, ?)
                """,
                (emotion, image_path, datetime.now()),
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the labeling emotions table: {e}",
            )

    def create_labeling_tiredness_table(self):
        # create a table to store labeling tiredness associated with user face images
        try:
            self.create_table(
                """
                CREATE TABLE IF NOT EXISTS labeling_tiredness (
                    id INTEGER PRIMARY KEY,
                    tiredness TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                )
                    """
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the labeling tiredness table: {e}",
            )
    def insert_into_tiredness_labeling(self, tiredness, image_path):
        # insert into labeling tiredness table
        try:
            self.insert_into_table(
                """
                INSERT INTO labeling_tiredness(tiredness, image_path, created_at)
                VALUES(?, ?)
                """,
                (tiredness, image_path, datetime.now()),
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the labeling tiredness table: {e}",
            )

    def create_labeling_mental_health(self):
        # create a table to store labeling mental health associated with user face images
        try:
            self.create_table(
                """
                CREATE TABLE IF NOT EXISTS labeling_mental_health (
                    id INTEGER PRIMARY KEY,
                    mental_health TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                )
                    """
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the labeling mental health table: {e}",
            )
    
    def insert_into_mental_health_labeling(self, mental_health, image_path):
        # insert into labeling mental health table
        try:
            self.insert_into_table(
                """
                INSERT INTO labeling_mental_health(mental_health, image_path, created_at)
                VALUES(?, ?)
                """,
                (mental_health, image_path, datetime.now()),
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the labeling mental health table: {e}",
            )

    def create_labeling_symptoms_concerns(self):
        # create a table to store labeling symptoms and concerns associated with user face images
        try:
            self.create_table(
                """
                CREATE TABLE IF NOT EXISTS labeling_symptoms_concerns (
                    id INTEGER PRIMARY KEY,
                    symptoms_concerns TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                )
                    """
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the labeling symptoms and concerns table: {e}",
            )
    
    def insert_into_symptoms_concerns_labeling(self, symptoms_concerns, image_path):
        # insert into labeling symptoms and concerns table
        try:
            self.insert_into_table(
                """
                INSERT INTO labeling_symptoms_concerns(symptoms_concerns, image_path, created_at)
                VALUES(?, ?)
                """,
                (symptoms_concerns, image_path, datetime.now()),
            )
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the labeling symptoms and concerns table: {e}",
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
