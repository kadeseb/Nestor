#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import os
import playsound
import random
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 250)
engine.say('Ceci est un test de synthèse vocale!')
engine.runAndWait()

exit(1)
r = sr.Recognizer()

def speak(text):
    filename = "_text.mp3"
    tts = gTTS(text=text, lang='fr')
    tts.save(filename)
    playsound.playsound(filename)
    #os.remove(filename)

def convertVoiceToText():
    while(True):
        with sr.Microphone() as source:
            print("<En écoute>")
            audio = r.listen(source)
        try:
            return r.recognize_sphinx(audio, language="fr-FR")
        except sr.UnknownValueError:
            speak("L'audio n'as pas été compris!")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

def detect_query():
    speak("En attente de mots clefs !");
    text = convertVoiceToText();
    print("Compris: " + text);
    speak("J'ai compris : " + text)

    if (text.find("assistant") != -1):
        return True
    else:
        return False

print("============================")
print("Démarrage du Projet Nestor !")
print("============================")
# speak("Test de synthèse vocale!");
quit=False

while(not quit):
    if detect_query():
        speak("Ok, requête détecté. En attente d'instruction !")

        while(True):
            query = convertVoiceToText();
            print(query);
            speak("J'ai compris : " + query)

            if (query == "quitter"):
                quit=True
                speak("Ok, arrêt du programme!")
                exit(0)

            elif (query == "continuer" or query == "continuait"):
                speak("Ok, le programme continue!")
                break
            else:
                speak("Instruction incorrecte !");

'''
while True:
    r  = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dites quelque chose")
        audio = r.listen(source)
    try:
        text = r.recognize_sphinx(audio, language="fr-FR" )
        print("Vous avez dit : " + text)
    except sr.UnknownValueError:
        print("L'audio n'as pas été compris!")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
'''
