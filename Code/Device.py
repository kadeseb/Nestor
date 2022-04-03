#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
Gère les équipements
'''

from datetime import datetime
# -------
import Attribute
import Command
import LEDPanel as DEV_LEDPanel
import Config

class Manager:
    def __init__(self):
        self.devices = []
        self.devices.append(General())
        self.devices.append(LEDPanel())

    def execute(self, query):
        device = None
        for dev in self.devices:
            if (dev.getName() == query.getTargetDevice()):
                device = dev
                break

        if (device == None):
            return Command.Answer(Command.Answer.CODE_ERROR_UNKNOW_DEVICE, Command.Answer.ERROR_CODE_TO_TEXT[Command.Answer.CODE_ERROR_UNKNOW_DEVICE])

        if (query.getMode() == Command.Query.MODE_READ):
            return device.get(query.getArgument().getName())
        else:
            return device.set(query.getArgument().getName(), query.getArgument().getValue())

class BaseDevice:
    def __init__(self):
        self.name = None
        self.attributes = []

    def isAttributeExists(self, attributeName):
        for attribute in self.attributes:
            if (attribute.getName() == attributeName):
                return True

        return False

    def getName(self):
        return self.name

    def getAttribute(self, attributeName):
        attr = None
        for attr in self.attributes:
            if (attributeName == attr.getName()):
                break

        return attr

    def get(self, attributName):
        ''' Méthode à surcharger '''

    def set(self, attributeName, attributeValue):
        ''' Méthode à surcharger '''

class General(BaseDevice):
    def __init__(self):
        super().__init__()
        self.name = "general"
        self.attributes.append(Attribute.ReadOnly("heure"))
        self.attributes.append(Attribute.ReadOnly("date"))
        self.attributes.append(Attribute.ReadOnly("temps"))

    def get(self, attributeName):
        r = Command.Answer(Command.Answer.CODE_ERROR_UNKNOW_ATTRIBUTE, Command.Answer.ERROR_CODE_TO_TEXT[Command.Answer.CODE_ERROR_UNKNOW_ATTRIBUTE])
        now = datetime.now()
        curTime = '{dt.hour} heure {dt.minute}'.format(dt=now)
        curDate = '{dt.day}/{dt.month}/{dt.year}'.format(dt=now)

        if (attributeName == "heure"):
            r = Command.Answer(Command.Answer.CODE_OK, "Il est %s." % (curTime))
        elif (attributeName == "date"):
            r =  Command.Answer(Command.Answer.CODE_OK, "Nous sommes le %s." % (curDate))
        elif (attributeName == "temps"):
            r = Command.Answer(Command.Answer.CODE_OK, "Nous sommes le %s, il est %s." % (curDate, curTime))

        return r

    def set(self, attributeName, attributeValue):
        return Command.Answer(Command.Answer.CODE_ERROR_READONLY_ATTRIBUTE, Command.Answer.ERROR_CODE_TO_TEXT[Command.Answer.CODE_ERROR_READONLY_ATTRIBUTE])

class LEDPanel(BaseDevice):
    def __init__(self):
        super().__init__()
        self.name = "bandeau"
        self.controller = DEV_LEDPanel.Controller(Config.LEDPANEL_MAC_ADDRESS)
        self.attributes.append(Attribute.Boolean("alimentation"))
        self.attributes.append(Attribute.Integer("luminosité"))
        self.attributes.append(Attribute.TextColor("couleur"))

    '''
    def __del__(self):
        self.controller.stopAdapter()
    '''

    def get(self, attributName):
        return Command.Answer(Command.Answer.CODE_ERROR_INVALID_VALUE, "Cet équipement ne supporte pas la lecture d'attribut.")

    def set(self, attributeName, attributeValue):
        r = Command.Answer(Command.Answer.CODE_ERROR_UNKNOW_ATTRIBUTE, Command.Answer.ERROR_CODE_TO_TEXT[Command.Answer.CODE_ERROR_UNKNOW_ATTRIBUTE])
        attribute = self.getAttribute(attributeName)

        if (attribute == None):
            return r

        r = attribute.setValue(attributeValue)
        if (r == False):
            return Command.Answer(Command.Answer.CODE_ERROR_INVALID_VALUE, Command.Answer.ERROR_CODE_TO_TEXT[Command.Answer.CODE_ERROR_INVALID_VALUE])

        if (attributeName == "alimentation"):
            if (attributeValue == "0"):
                self.controller.powerOff()
            else:
                self.controller.powerOn()
        elif (attributeName == "luminosité"):
            self.controller.setBrightness(int(attributeValue))
        elif (attributeName == "couleur"):
            self.controller.setColor(*attribute.getValue())

        return Command.Answer(Command.Answer.CODE_OK, "La valeur de l'attribut a été modifiée avec succèes !")
