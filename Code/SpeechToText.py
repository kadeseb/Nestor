#!/usb/bin/python
#! -*- coding: utf8 -*-
import speech_recognition as sr

'''
Gère la reconnaissance vocale
'''

class SpeechToText:
    TIMEOUT = 14.00
    PHRASE_TIME_LIMIT = 7.00
    ADJUST_DELAY = 3.0

    def __init__(self):
        self.r = sr.Recognizer()

    def calibrateAmbientNoise(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=self.ADJUST_DELAY)

    def listen(self):
        while(True):
            with sr.Microphone() as source:
                try:
                    print(">[STP] En écoute...")
                    audio = self.r.listen(source, timeout=self.TIMEOUT, phrase_time_limit=self.PHRASE_TIME_LIMIT)
                    return self.r.recognize_google(audio, language="fr-FR")
                except sr.UnknownValueError:
                    print(">[STP] L'audio n'a pas été compris!")
                except sr.RequestError as e:
                    print(">[STP] Erreur: Impossible d'obtenir des résultats depuis le service Google Cloud Speech; {0}".format(e))
                except sr.WaitTimeoutError:
                    print(">[STP] Erreur: Temps impartit écoulé.")
