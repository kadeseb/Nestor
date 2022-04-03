#!/usr/bin/python3
# -*- coding:utf8 -*-
'''
Gère la connexion Bluetooth avec le panneau LED
'''

import pygatt

class Controller:
    HANDLE = 0x08
    POWER_OFF_CMD = bytearray([0x7E, 0x04, 0x04, 0x00, 0x00, 0x00, 0xFF, 0x00, 0xEF])
    POWER_ON_CMD = bytearray([0x7E, 0x04, 0x04, 0xF0, 0x00, 0x01, 0xFF, 0x00, 0xEF])
    ADDRESS_TYPE = pygatt.BLEAddressType.public

    def __init__(self, macAddr):
        # Initialisation de l'adaptateur Bluetooth
        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start()
        self.macAddr = macAddr
        self.device = None

    def reconnectIfDisconnected(func):
        ''' Décorateur '''

        def wrapper(self, *args, **kwargs):
            try:
                if (self.device == None):
                    raise pygatt.exceptions.NotConnectedError

                return func(self, *args, **kwargs)
            except pygatt.exceptions.NotConnectedError:
                self._connect()
                return func(self, *args, **kwargs)

        return wrapper


    def _connect(self):
        while (True):
            try:
                print("[LEDPanel] Connexion au bandeau...")
                self.device = self.adapter.connect(self.macAddr)#, address_type=ADDRESS_TYPE)
                break
            except pygatt.exceptions.NotConnectedError as e:
                print("[LEDPanel] Erreur: La connexion à échoué !")

    def stopAdapter(self):
        self.adapter.stop()

    '''
    def __del__(self):
        self.adapter.stop()
    '''

    @reconnectIfDisconnected
    def powerOff(self):
        self.device.char_write_handle(self.HANDLE, self.POWER_OFF_CMD)

    @reconnectIfDisconnected
    def powerOn(self):
        self.device.char_write_handle(self.HANDLE, self.POWER_ON_CMD)

    @reconnectIfDisconnected
    def setColor(self, red, green, blue):
        self.device.char_write_handle(self.HANDLE, bytearray([0x7E, 0x07, 0x05, 0x03, red, green, blue, 0x10, 0xEF]))

    @reconnectIfDisconnected
    def setBrightness(self, brightness):
        self.device.char_write_handle(self.HANDLE, bytearray([0x7E, 0x04, 0x01, brightness, 0x01, 0xFF, 0xFF, 0x00, 0xEF]))
