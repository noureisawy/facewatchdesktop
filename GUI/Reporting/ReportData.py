from DB.Data import Data
from PyQt5.QtWidgets import QWidget, QLabel, QListWidgetItem, QHBoxLayout
import openai
# TODO: add the openai api key here
openai.api_key = "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"
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

prompt_formate = """
your task is to give me a report for users about their well being and health monitoring:

I am creating a desktop app that will capture an image for users while setting in front of the labtop this image will pass to a 
deep learning model it will extract user face from this image. then the face image will passed to the a machine model that will predict 
emotion for that user I am detecting 7 emotions "happy","neutral", "sad", "angry", "fear", "disgust", and "surprise" . also the face image
will passed to a deep learning model that will predict the level of alertness of the user it will output 3 levels "tired", "non_vigilant" and "alert".
the image will also passed to a deep learning model that will predict the liklihood of a symptomes or a diseases in face it will predict 
"Alopecia Hair Loss",
"Butterfly Rash Face",
"Dehydration Cracked Libs",
"Drooping Eyelid",
"Jaundice Yellowish Skin and Eyes",
"Melasma Face",
"Moles Face",
"Normal",
"Puffy Eyes Face",
"Sores in face",
"Stroke Face",
and "Xanthelasma Yellow Spots on Your Eyelids",

but don't give this model a lot of interests cause it only score 60% accuracy.

now I will give you the user emotions over time, and user level of alertness and the user symptoms and diseases prediction overtime and I want you
to 
1- summarize user emotions
2- summarize level of alertness
3- summarize symptoms and diseases prediction
4- give a user a report about all of that the report should be text in English. maximum length is 200 words. the report should give the user 
information about his well being. give him seggestion about what he should do if the there are overall a negative results.
it should give the user some motifiation about his will being and give him clues about activities to do.
5- the app name is Facewatch

the user data will be delimited with ``` 

here is the user data ```
emotions:

{emotions}


level of alertness:

{alertness}


diseases prediction:

{diseases}

```
give me the report that I will show it to the user

"""


class ReportData:
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget
        self.data = Data.get_instant()
        self.report = None
        self.report_data = None
        self.show_reports()

    def show_reports(self):
        self.report_data = self.data.get_all_reports()
        self.parent_widget.clear()
        for row in self.report_data:
            parent_widget = QWidget()
            layout = QHBoxLayout(parent_widget)
            label = QLabel(parent_widget)
            label.setWordWrap(True)
            label.setText(row[1])
            layout.addWidget(label)
            parent_widget.setStyleSheet(
                "QLabel, QListWidgetItem {font-size:20px; background-color : black; color : white; width:100%; border-radius: 20px; padding: 50px; }"
            )
            item = QListWidgetItem(self.parent_widget)
            item.setSizeHint(parent_widget.sizeHint())
            self.parent_widget.addItem(item)
            self.parent_widget.setItemWidget(item, parent_widget)
            # self.parent_widget.itemClicked.connect(self.show_report)
    
    def add_report(self):
        last_15_emotions_prediction = self.data.get_last_15_emotions_prediction()
        last_15_tiredness_prediction = self.data.get_last_15_tiredness_prediction()
        last_15_symptoms_prediction = self.data.get_last_15_symptoms_prediction()
        text = prompt_formate.format(emotions=last_15_emotions_prediction, alertness=last_15_tiredness_prediction, diseases=last_15_symptoms_prediction)
        report = get_completion(text)
        self.data.insert_report(report)
        self.show_reports()
