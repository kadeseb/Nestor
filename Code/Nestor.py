#!/usr/bin/python3
# -*- coding: utf8 -*-

# NOTE: this example requires PyAudio because it uses the Microphone class
#import speech_recognition as sr
import pyttsx3
import time
# -------
#from CommandAnalyzer2 import *
import Command
from WhistleDetector import *
from SpeechToText import *


'''
VOICE_RATE = 270
VOICE_RATE = 200
'''
VOICE_RATE = 200

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def setFrenchVoice(engine):
    voices = engine.getProperty('voices')

    for voice in voices:
        if (voice.name == "french"):
            engine.setProperty("voice", voice.id)
            return True

    return False

if (__name__ == "__main__"):
    # Initialisation de la synthèse vocale
    engine = pyttsx3.init();
    engine.setProperty('rate', VOICE_RATE)
    setFrenchVoice(engine)

    # Initialisation de l'analyseur de commande
    query = Command.Query()

    # Initialisation du détecteur de sifflement
    whistleDetect = WhistleDetector()

    # Initialisation de la reconnaissance vocale
    speechToText = SpeechToText()

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
            print("Commande comprise et exécuté !")
            query.show()
            speak("Commande comprise et exécuté !")
        else:
            '''
            error = cmdAnalyzer.getError()
            speak("Code erreur numéro %d, %s" % (cmdAnalyzer.getError(), cmdAnalyzer.getTextError()))
            '''
            speak("Erreur: syntaxe commande invalide !")
