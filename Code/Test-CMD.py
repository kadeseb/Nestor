#!/usr/bin/python3
# -*- coding: utf8 -*-

import Command
import Attribute
import pyttsx3

VOICE_RATE = 200
VOICE_NAME = "french-mbrola-4"

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

def listVoice(engine):
    voices = engine.getProperty('voices')

    for voice in voices:
        print(voice)

'''
COMMANDS = [
    'allume le bandeau',
    'modifie la luminosité à 25% du bandeau',
    'récupère la luminosité du bandeau',
    'modifie la couleur RGB en 255 255 255 du bandeau',
    'éteins le bandeau',
    'modifie la couleur en bleu du bandeau',
]
'''

'''
for command in COMMANDS
    print("Texte:", command)
    q = Command.Query()
    q.parse(command)
    q.show()
    print("")

'''
engine = pyttsx3.init();
engine.setProperty('rate', VOICE_RATE)
listVoice(engine)
setFrenchVoice(engine)
