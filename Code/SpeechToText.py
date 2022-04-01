#!/usb/bin/python
# -*- coding: utf8 -*-
'''
Gère la reconnaissance vocale
'''

import speech_recognition as sr
# -------
import Config

class SpeechToText:
    def __init__(self):
        self.r = sr.Recognizer()

    def calibrateAmbientNoise(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=Config.STT_ADJUST_DELAY)

    def listen(self):
        while(True):
            with sr.Microphone() as source:
                try:
                    print(">[STP] En écoute...")
                    audio = self.r.listen(source, timeout=Config.STT_TIMEOUT, phrase_time_limit=Config.STT_PHRASE_TIME_LIMIT)
                    return self.r.recognize_google(audio, language="fr-FR")
                except sr.UnknownValueError:
                    print(">[STP] L'audio n'a pas été compris!")
                except sr.RequestError as e:
                    print(">[STP] Erreur: Impossible d'obtenir des résultats depuis le service Google Cloud Speech; {0}".format(e))
                except sr.WaitTimeoutError:
                    print(">[STP] Erreur: Temps impartit écoulé.")
