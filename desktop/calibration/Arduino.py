# -*- coding: utf-8 -*-
"""
    ***********
    Arduino.py
    ***********
    
    Withholds a class which creates a serial connection with a micro controller.
"""
__author__ = 'Jonas Van Der Donckt'

import serial


class ArduinoSerial:
    def __init__(self, serial_port='/dev/ttyUSB0', baudrate=9600):
        """
        Creates an instance of a serial connection
        
        :param str serial_port: The serial port on which the micro controller is
            connected to the desktop (default: {'/dev/ttyUSB0'})
        :param int baudrate: The baud rate (bps) from the micro controller its serial
            port (default: {9600})
        """
        self.ser = serial.Serial(serial_port, baudrate)
        
    def read_serial(self):
        """
        Waits until the micro controller writes a new line to the serial connection,
        reads it and returns that line as a string. 
        
        :return: The value, written by the micro controller on the serial port
        :rtype: str
        """
        return self.ser.readline().decode('ascii')[:-1]
