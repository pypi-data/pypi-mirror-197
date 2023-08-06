import sys

import pyttsx3


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    text = sys.argv[1]
    speak(text)
