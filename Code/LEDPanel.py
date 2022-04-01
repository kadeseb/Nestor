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
        self.device = self.adapter.connect(macAddr)#, address_type=ADDRESS_TYPE)

        self.macAddr = macAddr

    def __del__(self):
        self.adapter.stop()

    def powerOff(self):
        self.device.char_write_handle(self.HANDLE, self.POWER_OFF_CMD)

    def powerOn(self):
        self.device.char_write_handle(self.HANDLE, self.POWER_ON_CMD)

    def setColor(self, red, green, blue):
        self.device.char_write_handle(self.HANDLE, bytearray([0x7E, 0x07, 0x05, 0x03, red, green, blue, 0x10, 0xEF]))

    def setBrightness(self, brightness):
        self.device.char_write_handle(self.HANDLE, bytearray([0x7E, 0x04, 0x01, brightness, 0x01, 0xFF, 0xFF, 0x00, 0xEF]))
