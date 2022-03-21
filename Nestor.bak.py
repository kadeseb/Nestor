#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
import speech_recognition as sr
import pyttsx3
import time

VOICE_RATE = 270

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    while(True):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            return r.recognize_google(audio, language="fr-FR") #recognize_sphinx
        except sr.UnknownValueError:
            speak("L'audio n'as pas été compris!")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))


if (__name__ == "__main__"):
    # Initialisation de la synthèse vocale
    engine = pyttsx3.init();
    engine.setProperty('rate', VOICE_RATE)
    print("[Nestor V1]");
    speak("Démarrage terminé...")
    while(True):
        speak("En écoute !");
        text = listen();
        print("Compris: " + text)
        speak("J'ai compris: " + text)

        if (text.find("quitter") != -1):
            speak("Compris !")
            speak("Arrêt du programme. Au revoir!");
            exit()
