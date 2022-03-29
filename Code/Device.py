#!/usr/bin/python3
# -*- coding: utf8 -*-
from datetime import datetime
# ---
import Attribute
import Command

class Manager:
    def __init__(self):
        self.devices = []
        self.devices.append(General())

    def execute(self, query):
        device = None
        for device in self.devices:
            if (device.getName() == query.getTargetDevice()):
                break

        if (device == None):
            return Command.Answer(Command.Answer.CODE_ERROR_UNKNOW_DEVICE, Command.Answer.ERROR_CODE_TO_TEXT[Command.Answer.CODE_ERROR_UNKNOW_DEVICE])

        if (query.getMode() == Command.Query.MODE_READ):
            return device.get(query.getArgument())
        else:
            return device.set(query.getArgument())

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


    def get(self, attribute):
        if (not self.isAttributeExists(attribute.getName())):
            return Command.Answer(Command.Answer.CODE_ERROR_UNKNOW_ATTRIBUTE, Command.Answer.ERROR_CODE_TO_TEXT[Command.Answer.CODE_ERROR_UNKNOW_ATTRIBUTE])

        ''' Méthode à surcharger '''

    def set(self, attribute):
        if (not self.isAttributeExists(attribute.getName())):
            return Command.Answer(Command.Answer.CODE_ERROR_UNKNOW_ATTRIBUTE, Command.Answer.ERROR_CODE_TO_TEXT[Command.Answer.CODE_ERROR_UNKNOW_ATTRIBUTE])

        # Recherche de l'attribut
        attr = None
        for attr in self.attributes:
            if (attribute.getName() == attr.getName()):
                break

        # Contrôle si l'attribut n'est pas en lecture seule
        if (attr.isReadOnly()):
            return Command.Answer(Command.Answer.CODE_ERROR_READONLY_ATTRIBUTE, Command.Answer.ERROR_CODE_TO_TEXT[Command.Answer.CODE_ERROR_READONLY_ATTRIBUTE])

        ''' Méthode à surcharger '''

class General(BaseDevice):
    def __init__(self):
        super().__init__()
        self.name = "general"
        self.attributes = []

        self.attributes.append(Attribute.ReadOnly("heure"))
        self.attributes.append(Attribute.ReadOnly("date"))
        self.attributes.append(Attribute.ReadOnly("temps"))

    def get(self, attribute):
        r = super().get(attribute)

        if (r != None):
            return r

        now = datetime.now()
        curTime = '{dt.hour} heure {dt.minute}'.format(dt=now)
        curDate = '{dt.day}/{dt.month}/{dt.year}'.format(dt=now)

        if (attribute.getName() == "heure"):
            attribute.setValue(curTime)
            r = Command.Answer(Command.Answer.CODE_OK, "Il est %s." % (curTime), attribute)
        elif (attribute.getName() == "date"):
            attribute.setValue(curDate)
            r =  Command.Answer(Command.Answer.CODE_OK, "Nous sommes le %s." % (curDate), attribute)
        elif (attribute.getName() == "temps"):
            attribute.setValue("%s %s" % (curTime, curDate))
            r = Command.Answer(Command.Answer.CODE_OK, "Nous sommes le %s, il est %s." % (curDate, curTime), attribute)

        return r
