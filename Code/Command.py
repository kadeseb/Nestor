#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Argument:
    '''
    Gère un argument
    '''
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value


class Query:
    '''
    Gère le parsing de requête
    '''
    # Mode d'opération
    MODE_READ = 1
    MODE_WRITE = 2

    # Mot-clefs correspondant au mode de fontionnement
    DEFAULT_DEVICE = 'general'
    KEYWORDS_READ_MODE = ["récupère", "recupere"]
    KEYWORDS_WRITE_MODE = ["modifie", "modifier", "change", "changer"]
    REMOVE_WORDS_LIST = ['le', 'la', 'de', 'du', 'à', 'pour', 'en', 'depuis', 'via', 'sur', "l'"]

    def __init__(self):
        self.mode = None
        self.argument = None
        self.targetDevice = None
        self.badCmd = True

    def parse(self, text):
        self.__init__()
        words = self._cleanWords(text.split(' '))
        wordsSz = len(words)

        print("Résultat parsing:", words)

        if ((wordsSz < 2) or (wordsSz > 4)):
            return False

        if (not self._identifyMode(words[0])):
            return False

        if (self.mode == self.MODE_READ):
            self.argument = Argument(words[1])
            targetDeviceIndex = 2
        else:
            self.argument = Argument(words[1], words[2])
            targetDeviceIndex = 3


        # Contrôle de la présence de l'équipement cible
        self.targetDevice = words[targetDeviceIndex] if ((wordsSz - 1) == targetDeviceIndex) else self.DEFAULT_DEVICE

        self.badCmd = False
        return True

    def _identifyMode(self, word):
        for readKeyword in self.KEYWORDS_READ_MODE:
            if (word == readKeyword):
                self.mode = self.MODE_READ
                return True

        for writeKeyword in self.KEYWORDS_WRITE_MODE:
            if (word == writeKeyword):
                self.mode = self.MODE_WRITE
                return True

        return False

    @staticmethod
    def _cleanWords(words):
        cleanWords = []

        for curWord in words:
            if (curWord in Command.REMOVE_WORDS_LIST):
                continue

            cleanWords.append(curWord)

        return cleanWords

    def getMode(self):
        return self.mode

    def getArgument(self):
        return self.argument

    def getTargetDevice(self):
        return self.targetDevice

    def isInvalid(self):
        return self.badCmd

    def show(self):
        if (self.badCmd):
            print ("{Requête invalide} !")
        else:
            print("Mode [%d] ; Arguments [%s : %s] ; Cible [%s]" % (self.mode, self.argument.getName(), self.argument.getValue(), self.targetDevice))
