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

    def __init__(self):
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
            # Create a table to store all the data which shared with the server
            self.create_shared_data_table()
            # Create a table to store all the data which shared with the server
            self.create_reporting_table()
            # Create a table to store diseases prediction
            self.create_diseases_prediction_table()

        except sqlite3.Error as e:
            print(f"An error occurred while connecting to the database: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while connecting to the database: {e}",
            )

    def get_last_15_emotions_prediction(self):
        # get last 15 emotions prediction
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM emotions ORDER BY timestamp DESC LIMIT 15
                """
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while getting last 15 emotions prediction: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while getting last 15 emotions prediction: {e}",
            )

    def get_last_15_tiredness_prediction(self):
        # get last 15 tiredness prediction
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM tiredness ORDER BY timestamp DESC LIMIT 15
                """
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while getting last 15 tiredness prediction: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while getting last 15 tiredness prediction: {e}",
            )

    def get_last_15_symptoms_prediction(self):
        # get last 15 symptoms prediction
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM diseases_prediction ORDER BY timestamp DESC LIMIT 15
                """
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while getting last 15 symptoms prediction: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while getting last 15 symptoms prediction: {e}",
            )

    def create_diseases_prediction_table(self):
        # create a table to store diseases prediction
        try:
            self.create_table(
                """
            CREATE TABLE IF NOT EXISTS diseases_prediction (
                id INTEGER PRIMARY KEY,
                diseases TEXT NOT NULL,
                timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
            )
            """
            )
        except sqlite3.Error as e:
            print(
                f"An error occurred while creating the diseases prediction table: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the diseases prediction table: {e}",
            )

    def add_disease_prediction(self, prediction):
        # add disease prediction
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO diseases_prediction(diseases)
                VALUES(?)
                """,
                (prediction,),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while adding disease prediction: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while adding disease prediction: {e}",
            )

    def create_reporting_table(self):
        # create a table to store reporting data
        try:
            self.create_table(
                """
            CREATE TABLE IF NOT EXISTS reporting (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                created_at NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
        except sqlite3.Error as e:
            print(f"An error occurred while creating the reporting table: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the reporting table: {e}",
            )

    def insert_report(self, text):
        # insert into reporting table
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO reporting(text)
                VALUES(?)
                """,
                (text,),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while inserting into the reporting table: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the reporting table: {e}",
            )

    def get_all_reports(self):
        # get all the data from the reporting table
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM reporting ORDER BY created_at DESC
                """
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(
                f"An error occurred while getting all the data from the reporting table: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while getting all the data from the reporting table: {e}",
            )

    def create_shared_data_table(self):
        # create a table to store all the data which shared with the server
        try:
            self.create_table(
                """
                CREATE TABLE IF NOT EXISTS shared_data (
                    id INTEGER PRIMARY KEY,
                    image_path TEXT NOT NULL,
                    label TEXT NOT NULL
                    )
            """
            )
        except sqlite3.Error as e:
            print(f"An error occurred while creating the shared data table: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the shared data table: {e}",
            )

    def insert_shared_data(self, label, image_path):
        # insert into shared data table
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO shared_data(image_path, label)
                VALUES(?, ?)
                """,
                (image_path, label),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while inserting into the shared data table: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the shared data table: {e}",
            )

    def check_if_data_shared_before(self, label, image_path):
        # check if data shared before
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM shared_data WHERE image_path = ? AND label = ?
                """,
                (image_path, label),
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while checking if data shared before: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while checking if data shared before: {e}",
            )

    def delete_sharing_data_table(self):
        # delete all the data in the sharing data table
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                DELETE FROM shared_data
                """
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the shared data table: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while deleting the shared data table: {e}",
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
            print(f"An error occurred while creating the labeling emotions table: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the labeling emotions table: {e}",
            )

    def insert_emotion_labeling(self, emotion, image_path):
        # insert into labeling emotions table
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO labeling_emotions(emotion, image_path, created_at)
                VALUES(?, ?, ?)
                """,
                (emotion, image_path, datetime.now()),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(
                f"An error occurred while inserting into the labeling emotions table: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the labeling emotions table: {e}",
            )

    def get_all_emotions_labeling(self):
        # get all emotions labeling
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM labeling_emotions ORDER BY created_at DESC")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while getting all emotions labeling: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while getting all emotions labeling: {e}",
            )

    def update_emotion_label(self, emotion, created_at):
        # update emotion labeling
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE labeling_emotions
                SET emotion = ?
                WHERE image_path = ?
                """,
                (emotion, created_at),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating emotion labeling: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while updating emotion labeling: {e}",
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
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                    """
            )
        except sqlite3.Error as e:
            print(f"An error occurred while creating the labeling tiredness table: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the labeling tiredness table: {e}",
            )

    def insert_tiredness_labeling(self, tiredness, image_path):
        # insert into labeling tiredness table
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO labeling_tiredness(tiredness, image_path, created_at)
                VALUES(?, ?, ?)
                """,
                (tiredness, image_path, datetime.now()),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(
                f"An error occurred while inserting into the labeling tiredness table: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the labeling tiredness table: {e}",
            )

    def get_all_tiredness_labeling(self):
        # get all tiredness labeling
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM labeling_tiredness ORDER BY created_at DESC")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while getting all tiredness labeling: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while getting all tiredness labeling: {e}",
            )

    def update_tiredness_label(self, tiredness, created_at):
        # update tiredness labeling
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE labeling_tiredness
                SET tiredness = ?
                WHERE image_path = ?
                """,
                (tiredness, created_at),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating tiredness labeling: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while updating tiredness labeling: {e}",
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
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                    """
            )
        except sqlite3.Error as e:
            print(
                f"An error occurred while creating the labeling mental health table: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the labeling mental health table: {e}",
            )

    def insert_mental_health_labeling(self, mental_health, image_path):
        # insert into labeling mental health table
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO labeling_mental_health(mental_health, image_path, created_at)
                VALUES(?, ?, ?)
                """,
                (mental_health, image_path, datetime.now()),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(
                f"An error occurred while inserting into the labeling mental health table: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the labeling mental health table: {e}",
            )

    def get_all_mental_health_labeling(self):
        # get all mental health labeling
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM labeling_mental_health ORDER BY created_at DESC"
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while getting all mental health labeling: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while getting all mental health labeling: {e}",
            )

    def update_mental_health_label(self, mental_health, created_at):
        # update mental health labeling
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE labeling_mental_health
                SET mental_health = ?
                WHERE image_path = ?
                """,
                (mental_health, created_at),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating mental health labeling: {e}")
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while updating mental health labeling: {e}",
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
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                    """
            )
        except sqlite3.Error as e:
            print(
                f"An error occurred while creating the labeling symptoms and concerns table: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while creating the labeling symptoms and concerns table: {e}",
            )

    def insert_symptoms_concerns_labeling(self, symptoms_concerns, image_path):
        # insert into labeling symptoms and concerns table
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO labeling_symptoms_concerns(symptoms_concerns, image_path, created_at)
                VALUES(?, ?, ?)
                """,
                (symptoms_concerns, image_path, datetime.now()),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(
                f"An error occurred while inserting into the labeling symptoms and concerns table: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while inserting into the labeling symptoms and concerns table: {e}",
            )

    def get_all_symptoms_concerns_labeling(self):
        # get all symptoms and concerns labeling
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM labeling_symptoms_concerns ORDER BY created_at DESC"
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(
                f"An error occurred while getting all symptoms and concerns labeling: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while getting all symptoms and concerns labeling: {e}",
            )

    def update_symptoms_concerns_label(self, symptoms_concerns, created_at):
        # update symptoms and concerns labeling
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE labeling_symptoms_concerns
                SET symptoms_concerns = ?
                WHERE image_path = ?
                """,
                (symptoms_concerns, created_at),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(
                f"An error occurred while updating symptoms and concerns labeling: {e}"
            )
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while updating symptoms and concerns labeling: {e}",
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
            print(f"An error occurred while creating the tiredness table: {e}")
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
                    created_at DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                    last_emotion_update DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                    last_alertness_update DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                    last_mental_health_update DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                    last_symptoms_update DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
                )
                    """
            )
            # create first user information
            self.create_user_information()

        except sqlite3.Error as e:
            print(f"An error occurred while creating the user information table: {e}")
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
            print(f"An error occurred while creating the emotions table: {e}")
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
            print(f"An error occurred while retrieving user information: {e}")
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
                print(f"An error occurred while retrieving data: {e}")
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
                print(f"An error occurred while retrieving data: {e}")
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
                print(f"An error occurred while deleting data: {e}")
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
                print(f"An error occurred while deleting data: {e}")
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
            print(f"An error occurred while inserting data: {e}")
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
                last_emotion_update = datetime.now()
                cursor.execute(
                    """
                    UPDATE user_information SET current_emotion = ?, last_emotion_update = ? WHERE id = 1
                    """,
                    (
                        current_emotion,
                        last_emotion_update,
                    ),
                )
            if alertness_state:
                last_alertness_update = datetime.now()
                cursor.execute(
                    """
                    UPDATE user_information SET alertness_state = ?, last_alertness_update = ? WHERE id = 1
                    """,
                    (
                        alertness_state,
                        last_alertness_update,
                    ),
                )
            if current_mental_health:
                last_mental_health_update = datetime.now()
                cursor.execute(
                    """
                    UPDATE user_information SET current_mental_health = ?, last_mental_health_update = ? WHERE id = 1
                    """,
                    (
                        current_mental_health,
                        last_mental_health_update,
                    ),
                )
            if current_symptoms_concerns:
                last_symptoms_update = datetime.now()
                cursor.execute(
                    """
                    UPDATE user_information SET current_symptoms_concerns = ?, last_symptoms_update = ? WHERE id = 1
                    """,
                    (
                        current_symptoms_concerns,
                        last_symptoms_update,
                    ),
                )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating user information: {e}")
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
            print(f"An error occurred while creating user information: {e}")

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
            print(f"An error occurred while inserting data: {e}")
            QMessageBox.critical(
                None, "Error", f"An error occurred while inserting data: {e}"
            )
