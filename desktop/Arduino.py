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
        """
        Creates an instance of a Serial connection
        
        :param str serialport: The serial port on which the microcontroller is 
            connected to the desktop on which this code is running (default: {'/dev/ttyUSB0'})
        :param int baudrate: The baudrate of the Serial port from the micronctroller (default: {9600})
        """
        self.ser = serial.Serial(serialport, baudrate)
        
    def readSerial(self):
        """
        Waits until the microcontroller sends writes a new line to the Serial
        connection, reads it and return the line as a string. 
        
        :return: The read value
        :rtype: str
        """
        return self.ser.readline().decode('ascii')[:-1]
