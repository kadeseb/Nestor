#!/usb/bin/python
#! -*- coding: utf8 -*-
import speech_recognition as sr

def listen():

    ad = False
    while(True):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if (not ad):
                r.adjust_for_ambient_noise(source)
                ad = True

            print(">[STP] En écoute...")
            audio = r.listen(source)
        try:
            return r.recognize_google(audio, language="fr-FR")
        except sr.UnknownValueError:
            print(">[STP] L'audio n'as pas été compris!")
        except sr.RequestError as e:
            print(">[STP] Erreur: Impossible d'obtenir des résultats depuis le service Google Cloud Speech; {0}".format(e))
