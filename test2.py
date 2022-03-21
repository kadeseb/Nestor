#!/usr/bin/python3
#! -*- coding: utf-8 -*-

#from CommandAnalyzer import *
from Command import *

COMMANDS = [
    'allume le bandeau',
    'change la luminosité à 25% du bandeau',
    'récupère la luminosité du bandeau',
    'change la couleur RGB en 255 255 255 du bandeau',
    'éteins le bandeau',
    'change la couleur en bleu du bandeau',
]

REMOVE_WORDS = ['le', 'la', 'de', 'du', 'à', 'pour', 'en']

def cleanCommand(command):
    for word in REMOVE_WORDS:
        command = command.replace(' %s ' %  (word), ' ')
        command = command.lower()

    return command

if (__name__ == '__main__'):
    for command in COMMANDS:
        print("Avant:", command)
        print("Après:", cleanCommand(command))
        print("")
