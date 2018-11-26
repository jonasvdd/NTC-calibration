# -*- coding: utf-8 -*-
"""
    ***********
    Arduino.py
    ***********
    
    Withholds a class which creates a serial connection with a microcontroller.
"""
__author__ = 'Jonas Van Der Donckt'

import serial


class ArduinoSerial:
    def __init__(self, serialport='/dev/ttyUSB0', baudrate=9600):
        """
        Creates an instance of a serial connection
        
        :param str serialport: The serial port on which the microcontroller is 
            connected to the desktop (default: {'/dev/ttyUSB0'})
        :param int baudrate: The baud rade (bps) from the microcontroller its serial
            port (default: {9600})
        """
        self.ser = serial.Serial(serialport, baudrate)
        
    def readSerial(self):
        """
        Waits until the microcontroller writes a new line to the serial connection, 
        reads it and returns that line as a string. 
        
        :return: The value, written by the microcontroller on the serial port
        :rtype: str
        """
        return self.ser.readline().decode('ascii')[:-1]
