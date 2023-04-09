from DB.Data import Data
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
import time

class User:
    __gender = {
        "man": 0,
        "woman": 1,
    }
    __emotions = {
        "neutral": 0,
        "happy": 1,
        "surprise": 2,
        "angry": 3,
        "sad": 4,
        "fear": 5,
        "disgust": 6,
    }
    __alertness = {
        "alert": 0,
        "non_vigilant": 1,
        "tired": 2,
    }

    def __init__(self, window):
        self.window = window
        self.birth_year = None
        self.gender = None
        self.current_emotion = None
        self.alertness_state = None
        self.current_mental_health = None
        self.medical_history = None
        self.current_symptoms_concerns = None
        self.last_update_current_emotion = None
        self.last_update_alertness_state = None
        self.last_update_current_mental_health = None
        self.data = Data.get_instant()
        self.get_information()

    def get_information(self):
        row = self.data.get_user_information()
        print("row: ", row)
        row = row[0]
        self.birth_year = row[1]
        self.window.ui.birthYear.setText(
            str(self.birth_year) if self.birth_year else ""
        )
        self.window.ui.birthYear.textChanged.connect(self.handle_birth_year_changed)

        self.gender = row[2]
        self.window.ui.gender.setCurrentIndex(User.__gender.get(self.gender, 0))
        self.window.ui.gender.currentIndexChanged.connect(self.handle_gender_changed)

        self.current_emotion = row[3]
        self.window.ui.currentEmotion.setCurrentIndex(
            User.__emotions.get(self.current_emotion, 0)
        )
        self.window.ui.currentEmotion.currentIndexChanged.connect(
            self.handle_current_emotion_changed
        )

        self.alertness_state = row[4]
        self.window.ui.alertnessState.setCurrentIndex(
            User.__alertness.get(self.alertness_state, 0)
        )
        self.window.ui.alertnessState.currentIndexChanged.connect(
            self.handle_alertness_state_changed
        )

        self.current_mental_health = row[5]
        self.window.ui.currentMentalHealth.setPlainText(self.current_mental_health)
        self.window.ui.currentMentalHealth.textChanged.connect(
            self.handle_current_mental_health_changed
        )

        self.medical_history = row[6]
        self.window.ui.medicalHistory.setPlainText(self.medical_history)
        self.window.ui.medicalHistory.textChanged.connect(
            self.handle_medical_history_changed
        )

        self.current_symptoms_concerns = row[7]
        self.window.ui.currentSymptomsConcerns.setPlainText(
            self.current_symptoms_concerns
        )
        self.window.ui.currentSymptomsConcerns.textChanged.connect(
            self.handle_current_symptoms_concerns_changed
        )

    def handle_birth_year_changed(self):
        # check if text is a number
        text = self.window.ui.birthYear.toPlainText()
        if text.isdigit() & (len(text) <= 4):
            self.set_birth_year(text)
        elif len(text) > 4:
            QMessageBox.warning(None, "Warning", "Birth year must be 4 digits")
            self.window.ui.birthYear.setText(self.birth_year)
        else:
            QMessageBox.warning(None, "Warning", "Birth year must be a number")
            self.window.ui.birthYear.setText(self.birth_year)

    def handle_gender_changed(self, index):
        self.set_gender(self.window.ui.gender.itemText(index))

    def handle_current_emotion_changed(self, index):
        self.set_current_emotion(self.window.ui.currentEmotion.itemText(index))

    def handle_alertness_state_changed(self, index):
        self.set_alertness_state(self.window.ui.alertnessState.itemText(index))

    def handle_current_mental_health_changed(self):
        self.set_current_mental_health(self.window.ui.currentMentalHealth.toPlainText())

    def handle_medical_history_changed(self):
        self.set_medical_history(self.window.ui.medicalHistory.toPlainText())

    def handle_current_symptoms_concerns_changed(self):
        self.set_current_symptoms_concerns(
            self.window.ui.currentSymptomsConcerns.toPlainText()
        )

    def set_birth_year(self, birth_year):
        self.birth_year = birth_year
        self.data.update_user_information(birth_year=birth_year)

    def get_birth_year(self):
        return self.birth_year

    def set_gender(self, gender):
        self.gender = gender
        self.data.update_user_information(gender=gender)

    def get_gender(self):
        return self.gender

    def set_current_emotion(self, current_emotion):
        self.last_update_current_emotion = time.strftime("%Y%m%d-%H%M%S")
        self.current_emotion = current_emotion
        self.data.update_user_information(current_emotion=current_emotion)

    def get_current_emotion(self):
        return self.current_emotion

    def set_alertness_state(self, alertness_state):
        self.alertness_state = alertness_state
        self.last_update_alertness_state = time.strftime("%Y%m%d-%H%M%S")
        self.data.update_user_information(alertness_state=alertness_state)

    def get_alertness_state(self):
        return self.alertness_state

    def set_current_mental_health(self, current_mental_health):
        self.current_mental_health = current_mental_health
        self.last_update_current_mental_health = time.strftime("%Y%m%d-%H%M%S")
        self.data.update_user_information(current_mental_health=current_mental_health)

    def get_current_mental_health(self):
        return self.current_mental_health

    def set_medical_history(self, medical_history):
        self.medical_history = medical_history
        self.data.update_user_information(medical_history=medical_history)

    def get_medical_history(self):
        return self.medical_history

    def set_current_symptoms_concerns(self, current_symptoms_concerns):
        self.current_symptoms_concerns = current_symptoms_concerns
        self.data.update_user_information(
            current_symptoms_concerns=current_symptoms_concerns
        )

    def get_current_symptoms_concerns(self):
        return self.current_symptoms_concerns
