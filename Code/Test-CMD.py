#!/usr/bin/python3
# -*- coding: utf8 -*-

import Command

COMMANDS = [
    'allume le bandeau',
    'modifie la luminosité à 25% du bandeau',
    'récupère la luminosité du bandeau',
    'modifie la couleur RGB en 255 255 255 du bandeau',
    'éteins le bandeau',
    'modifie la couleur en bleu du bandeau',
]

for command in COMMANDS:
    print("Texte:", command)
    q = Command.Query()
    q.parse(command)
    q.show()
    print("")
