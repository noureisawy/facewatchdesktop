from Data import Data


data = Data()
# insert some emotional data
data.insert_emotion(
    {
        "emotion": {
            "angry": 0.0,
            "disgust": 0.0,
            "fear": 0.0,
            "happy": 0.0,
            "sad": 0.0,
            "surprise": 0.0,
            "neutral": 1.0,
        },
        "dominant_emotion": "neutral",
    }
)

data.insert_emotion(
    {
        "emotion": {
            "angry": 1.0,
            "disgust": 0.0,
            "fear": 0.0,
            "happy": 0.0,
            "sad": 0.0,
            "surprise": 0.0,
            "neutral": 0.0,
        },
        "dominant_emotion": "angry",
    }
)

data.insert_emotion(
    {
        "emotion": {
            "angry": 0.0,
            "disgust": 1.0,
            "fear": 0.0,
            "happy": 0.0,
            "sad": 0.0,
            "surprise": 0.0,
            "neutral": 0.0,
        },
        "dominant_emotion": "disgust",
    }
)

data.insert_emotion(
    {
        "emotion": {
            "angry": 0.0,
            "disgust": 0.0,
            "fear": 0.0,
            "happy": 0.0,
            "sad": 1.0,
            "surprise": 0.0,
            "neutral": 0.0,
        },
        "dominant_emotion": "sad",
    }
)

# get all data
print(data.get_date_between("2021-03-23 14:47:00", "2023-04-23 14:49:00"))
