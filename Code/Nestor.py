#!/usr/bin/python3
# -*- coding: utf8 -*-

# NOTE: this example requires PyAudio because it uses the Microphone class
#import speech_recognition as sr
import pyttsx3
import time
# -------
from WhistleDetector import *
from SpeechToText import *
import Command
import Device


VOICE_RATE = 200
VOICE_NAME = "french"

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def setFrenchVoice(engine):
    voices = engine.getProperty('voices')

    for voice in voices:
        if (voice.name == VOICE_NAME):
            engine.setProperty("voice", voice.id)
            return True

    return False

if (__name__ == "__main__"):
    # Initialisation de la synthèse vocale
    engine = pyttsx3.init();
    # engine.setProperty('rate', VOICE_RATE)
    setFrenchVoice(engine)

    # Initialisation du détecteur de sifflement
    whistleDetect = WhistleDetector()

    # Initialisation de la reconnaissance vocale
    speechToText = SpeechToText()

    # Initialisation de l'analyseur de requête
    query = Command.Query()

    # Initialisation du gestionnaire d'équipement
    devManager = Device.Manager()

    print("[Nestor V1]");
    speak("Calibration du bruit ambiant en cours...")
    speechToText.calibrateAmbientNoise()
    speak("Calibration terminée !")
    speak("Démarrage terminé ! Sifflez pour commander.");

    while(True):
        print("En attente d'un sifflement...")
        whistleDetect.waitForWhistle()
        print("Sifflement détecté...")

        speak("En écoute d'une commande !")
        text = speechToText.listen();
        if (query.parse(text)):
            query.show()
            speak("Syntaxe commande valide !")
        else:
            speak("Erreur : Syntaxe commande invalide !")
            continue

        # Execution de la requête
        answer = devManager.execute(query)

        if (answer.getCode() == 0):
            speak("La requête a été exécuté avec succès !")
        else:
            speak("La requête a échoué !")

        speak(answer.getMessage())
