#!/usr/bin/python3
# -*- coding: utf8 -*-
from datetime import datetime
# ---
import Attribute
import Command
import LEDPanel as DEV_LEDPanel

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

        self.attributes.append(Attribute.Boolean("alimentation"))
        self.attributes.append(Attribute.Integer("luminosité"))

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

        controller = DEV_LEDPanel.Controller('BE:89:A0:04:6D:92')

        if (attributeName == "alimentation"):
            if (attributeValue == "0"):
                controller.powerOff()
            else:
                controller.powerOn()
        elif (attributeName == "luminosité"):
            controller.setBrightness(int(attributeValue))
        controller.stopAdapter()

        return Command.Answer(Command.Answer.CODE_OK, "La valeur de l'attribut a été modifiée avec succèes !")
