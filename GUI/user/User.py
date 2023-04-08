
from DB.Data import Data

class User:
    def __init__(self):
        self.birth_year = None
        self.gender = None
        self.current_emotion = None
        self.alertness_state = None
        self.current_mental_health = None
        self.medical_history = None
        self.current_symptoms_concerns = None
        self.data = Data.get_instant()

    def get_information(self):
        row = self.Data.get_user_information()
        print("row: ", row)
        self.birth_year = row[0]
        self.gender = row[1]
        self.current_emotion = row[2]
        self.alertness_state = row[3]
        self.current_mental_health = row[4]
        self.medical_history = row[5]
        self.current_symptoms_concerns = row[6]
    
    # Create a setter and getter for each attribute
    def set_birth_year(self, birth_year):
        self.birth_year = birth_year
        self.data.update_user_information(birth_year = birth_year)

    def get_birth_year(self):
        return self.birth_year
    

    def set_gender(self, gender):
        self.gender = gender
        self.data.update_user_information(gender=gender)
    

    def get_gender(self):
        return self.gender
    
    def set_current_emotion(self, current_emotion):
        self.current_emotion = current_emotion
        self.data.update_user_information(current_emotion=current_emotion)
    
    def get_current_emotion(self):
        return self.current_emotion
    
    def set_alertness_state(self, alertness_state):
        self.alertness_state = alertness_state
        self.data.update_user_information(alertness_state=alertness_state)

    def get_alertness_state(self):
        return self.alertness_state
    
    def set_current_mental_health(self, current_mental_health):
        self.current_mental_health = current_mental_health
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
        self.data.update_user_information(current_symptoms_concerns=current_symptoms_concerns)
    
    def get_current_symptoms_concerns(self):
        return self.current_symptoms_concerns
    
        
        
        



