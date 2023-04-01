import sqlite3
from PyQt5.QtWidgets import QMessageBox

db_path = "C:/Users/UG/Desktop/research/FaceWatch/GUI/DB/emotions.db"

class Data:
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
