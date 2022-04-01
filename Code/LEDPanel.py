#!/usr/bin/python3
# -*- coding:utf8 -*-

'''
Gère un panneau LED
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

        while (True):
            try:
                self.device = self.adapter.connect(macAddr)#, address_type=ADDRESS_TYPE)
                break
            except:
                print("La connexion au bandeau a échoué ! Nouvelle tentative...")
                continue

    def _connect(self):
        while (True):
            try:
                print("[LEDPanel] Connexion au bandeau...")
                self.device = self.adapter.connect(macAddr)#, address_type=ADDRESS_TYPE)
                break
            except:
                print("[LEDPanel] La connexion au bandeau a échoué !")
                continue

    def _disconnect(self):
        self.device.disconnect()

    def stopAdapter(self):
        self.adapter.stop()

    '''
    def __del__(self):
        self.adapter.stop()
    '''

    def powerOff(self):
        self._connect()
        self.device.char_write_handle(self.HANDLE, self.POWER_OFF_CMD)

        self._disconnect()
    def powerOn(self):
        self._connect()
        self.setColor(0, 0, 255)
        self.device.char_write_handle(self.HANDLE, self.POWER_ON_CMD)
        self._disconnect()

    def setColor(self, red, green, blue):
        self._connect()
        self.device.char_write_handle(self.HANDLE, bytearray([0x7E, 0x07, 0x05, 0x03, red, green, blue, 0x10, 0xEF]))
        self._disconnect()

    def setBrightness(self, brightness):
        self._connect()
        self.device.char_write_handle(self.HANDLE, bytearray([0x7E, 0x04, 0x01, brightness, 0x01, 0xFF, 0xFF, 0x00, 0xEF]))
        self._disconnect()
