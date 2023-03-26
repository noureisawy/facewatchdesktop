from PyQt5.QtGui import QIcon
import random

class Notification:
    def show_tray_message(self, message):
        notificationTitle = "Face Watch Emotion Tracking"
        notificationMessage = message
        icon = QIcon("public/logo.png")
        duration = 3 * 1000
        self.tray.showMessage(notificationTitle, notificationMessage, icon, duration)

    def __init__(self, tray):
        self.tray = tray

    def show_notification(self, emotion):
        emotions_notifications = {
            "happy": [
                "That's great that you're feeling happy! Keep up the good work.",
                "I'm glad to see you're smiling.",
                "Enjoy this moment and savor the happiness.",
            ],
            "sad": [
                "I'm sorry to see you're feeling sad. I hope you feel better soon.",
                "Remember that sadness is temporary and you will feel better soon.",
                "I'm sorry that you're feeling sad.",
                "It's okay to cry and let out your emotions.",
            ],
            "angry": [
                "I'm sorry to see you're feeling angry. I hope you feel better soon.",
                "Remember that anger is temporary and you will feel better soon.",
                "I'm sorry that you're feeling angry.",
                "I'm sorry that you're feeling angry.",
                "It's okay to feel angry, but let's try to find a healthy way to express it.",
                "Take a deep breath and try to release the anger.",
            ],
            "surprised": [
                "I'm glad to see you're feeling surprised. I hope you're having a good day.",
                "That's a big surprise! How do you feel about it?",
                "I hope this surprise brings you joy and excitement.",
                "Sometimes surprises can be scary, but remember that it's okay to take your time processing it.",
            ],
            "disgusted": [
                "I'm sorry to see you're feeling disgusted. I hope you feel better soon.",
                "I'm sorry that you're feeling disgusted.",
                "Sometimes things can be gross or unpleasant, but we can get through it together.",
                "Remember that it's okay to feel disgusted, but try to focus on something positive instead.",
            ],
            "neutral": [
                "You seem to be feeling neutral. Is there anything you would like to talk about?",
                "Sometimes it's okay to not feel anything in particular.",
                "Take some time to relax and recharge.",
            ],
            "fear": [
                "Don't worry, everything is going to be okay.",
                "Take a deep breath and try to relax.",
                "It's okay to feel scared, but remember that you're not alone.",
            ],
        }
        if emotion in emotions_notifications:
            self.show_tray_message(
                random.choice(emotions_notifications[emotion])
            )
