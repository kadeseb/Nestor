#!/usr/bin/python3
# -*- coding: utf8 -*-

class BaseAttribute:
    TYPE_READONLY = 1
    TYPE_INTEGER = 2
    TYPE_BOOLEAN = 3

    def __init__(self, name):
        # if (not BaseAttribute.isTypeValid(type)):
        #     raise Exception("Le type de l'attribut est invalide !")

        self.name = name
        self.type = None
        self.value = None
        self.readOnly = False

    @staticmethod
    def isTypeValid(type):
        return (type == BaseAttribute.TYPE_READONLY) or (type == BaseAttribute.TYPE_INTEGER)

    def isValueValid(self, value):
        ''' Méthode à surcharger '''
        return False

    def isReadOnly(self):
        return self.readOnly

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def setValue(self, value):
        if (not self.isValueValid(value)):
            return False

        self.value = value
        return True


class ReadOnly(BaseAttribute):
    '''
    Attribut en lecture seule
    '''
    def __init__(self, name):
        super().__init__(name)
        self.readOnly = True
        self.type = BaseAttribute.TYPE_READONLY

    def setValue(self, value):
        return False

class Integer(BaseAttribute):
    '''
    Attribut étant un entier dans une intervalle de valeur
    '''
    def __init__(self, name):
        super().__init__(name)
        self.type = BaseAttribute.TYPE_INTEGER
        self.min = 0
        self.max = 255

    def setRange(self, min, max):
        if ((min < 0) or (max < 0) or (max < min)):
            return False

        self.min = min
        self.max = max
        return True

    def isValueValid(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

class Boolean(BaseAttribute):
    def __init__(self, name):
        super().__init__(name)
        self.type = BaseAttribute.TYPE_BOOLEAN

    def isValueValid(self, value):
        return (value == '0') or (value == '1')
