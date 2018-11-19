# -*- coding: utf-8 -*-
"""
    ***********
    Arduino.py
    ***********
    
    Withholds a class wich creates a serial connection with a microcontroller.
"""
__author__ = 'Jonas Van Der Donckt'

import serial


class ArduinoSerial:
    def __init__(self, serialport='/dev/ttyUSB0', baudrate=9600):
        self.ser = serial.Serial(serialport, baudrate)
        
    def readSerial(self):
        return self.ser.readline().decode('ascii')[:-1]
