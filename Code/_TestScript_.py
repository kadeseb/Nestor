#!/usr/bin/python3
# -*- coding: utf8 -*-

from LEDPanel import *
from time import sleep

LEDPANEL_MAC_ADDR = 'BE:89:A0:04:6D:92'

if (__name__ == '__main__'):
    LEDPANEL_MAC_ADDR = 'BE:89:A0:04:6D:92'
    led = LED(LEDPANEL_MAC_ADDR)

    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255)
    ]

    for i in range(0, 6):
        led.powerOn()
        led.setColor(*(colors[i%2]))
        sleep(3)
        led.powerOff()
