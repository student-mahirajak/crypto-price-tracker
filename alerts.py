import pyttsx3
from plyer import notification

def voice_alert(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def desktop_alert(message):
    notification.notify(
        title='🚨 Crypto Price Alert',
        message=message,
        timeout=5
    )
