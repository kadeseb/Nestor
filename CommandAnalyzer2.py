#!/usr/bin/python3
#! -*- coding: utf-8 -*-

from Command import *

'''
Analyse une chaine de caractère à la recherche d'une commande
'''

class CommandAnalyzer:
    KEYWORD = "Nestor"
    CMD_LIST = ["allume", "éteins"]
    CMD_DEVICES = ["bandeau"]
    CMD_ERROR_NO_QUERY = 1
    CMD_ERROR_INVALID_ACTION = 2
    CMD_ERROR_MULTIPLE_ACTION = 3
    CMD_ERROR_INVALID_DEVICE = 4
    CMD_ERROR_MULTIPLE_DEVICE = 5
    CMD_ERRORS = {
        1: "Mot-clef non détecté !",
        2: "L'action n'existe paz !",
        3: "Plusieurs actions ont été détectées !",
        4: "L'équipement cible n'existe pas !"
    }

    def __init__(self):
        self.result = False
        self.error = 0
        self.command = None

    def analyzeText(self, text):
        '''
        Analyse le texte fourni à la recherche d'une commande
        '''
        # # Vérification de la présence du mot-clef
        # keywordPos = text.find(self.KEYWORD)
        #
        # if (keywordPos == -1):
        #     self.error = self.CMD_ERROR_NO_QUERY
        #     return False

        # Analyse de la commande
        command = text#[len(self.KEYWORD) + keywordPos:].lower()

        # Analyze de l'action
        r = self._analyzeAction(command)
        if (r == None):
            return False
        action = r
        print("Action ->", action)

        # Analyze de l'équipement
        r = self._analyzeDevice(command)
        if (r == None):
            return False
        device = r
        print("Device ->", device)

        self.command = {
            "action": action,
            "device": device
        }
        return True

    def _analyzeAction(self, command):
        '''
        Analyze l'action à effectuer
        '''
        action = None

        for searchWord in self.CMD_LIST:
            if (command.find(searchWord) != -1):
                if (action != None):
                    self.error = self.CMD_ERROR_MULTIPLE_ACTION
                    return None
                action = searchWord

        if (action == None):
            self.error = self.CMD_ERROR_INVALID_ACTION
            return None

        return action

    def _analyzeDevice(self, command):
        '''
        Analyse l'équipement cible
        '''
        device = None

        for searchWord in self.CMD_DEVICES:
            if (command.find(searchWord) != -1):
                if (device != None):
                    self.error = self.CMD_ERROR_MULTIPLE_DEVICES
                    return None
                device = searchWord

        if (device == None):
            self.error = self.CMD_ERROR_INVALID_DEVICE
            return None

        self.error = 0
        return device

    def getResult(self):
        return self.state

    def getError(self):
        return self.error

    def getCommand(self):
        return self.command

    def getTextError(self):
        return self.CMD_ERRORS[self.error]
