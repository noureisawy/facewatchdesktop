from PyQt5.QtGui import QIcon
import random


class Notification:
    def show_tray_message(self, message, title="Face Watch Emotion Tracking"):
        notificationTitle = title
        notificationMessage = message
        icon = QIcon("public/logo.png")
        duration = 5 * 1000
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
            "tired": [
                "It's important to listen to your body and take breaks when you're feeling tired. Your health and well-being should always come first.",
                "Don't be afraid to delegate tasks or ask for help if you're feeling too tired to handle everything on your own.",
                "A good night's sleep can do wonders for your energy levels. Try to establish a consistent sleep routine to help combat feelings of tiredness throughout the day.",
            ],
            "non_vigilant": [
                "Sometimes it can be hard to stay alert, especially when you're dealing with a lot of stress. Take a few deep breaths and try to recenter yourself.",
                "If you're finding it difficult to focus, try breaking up your tasks into smaller, more manageable chunks. This can help you stay on track and avoid feeling overwhelmed.",
                "Remember to take care of your physical health as well. Getting regular exercise and eating a balanced diet can help boost your energy levels and increase your overall alertness.",
            ],
            "alert": [
                "You're doing great! Keep up the good work and stay focused on your goals.",
                "Take advantage of your alertness by tackling some of your more challenging tasks while you're feeling energized and engaged.",
                "Don't forget to take breaks and give yourself some downtime, even when you're feeling alert and productive. It's important to maintain a healthy work-life balance.",
            ],
        }
        if emotion in emotions_notifications:
            self.show_tray_message(
                random.choice(
                    emotions_notifications[emotion],
                ),
                title=f'Face Watch Emotion Tracking "{emotion}"',
            )
