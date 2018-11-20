# -*- coding: utf-8 -*-
"""
    *********
    main.py
    *********
    
    Starting point of the application. 
    TODO
"""
__author__ = 'Jonas Van Der Donckt'

from SteinhartHart import SteinHart
from Arduino import ArduinoSerial
from TSP01 import TSP01


#######################
#      constants
#######################
# Serial communication with the microcontroller
BAUDRATE =      9600
PORT =          '/dev/ttyUSB1'

CSVFILE =       'results.csv'

# Measurement board dependent variables
SERIALRESISTOR ='47400'
ACCURACYADC =   1023

if __name__ == '__main__':
    # Initialize the key objects
    tsp01 = TSP01()                         # accurate Temperature logger
    serial = ArduinoSerial(PORT, BAUDRATE)  # serial monitor to retrieve ADC value
    sth = SteinHart()                     # calculating and calibration the Steinhart-Hart equation/coefficients

    def v_devider_rntc(adc_val):
        return adc_val * SERIALRESISTOR / (ACCURACYADC - adc_val)

    while(True):
        adc_val = serial.readSerial()
        print("arduino serial: ", int(adc_val))

        ntcResistance =  v_devider_rntc(adc_val)
        print("ntc resistance: %s ohm" % ntcResistance)
        temperature = tsp01.probe_1_temperature()
        print("probe temprature: %s " % temperature)

        # feed the data so it can be used for calibration
        sth.feed(temperature, ntcResistance)

        with open(CSVFILE, mode='a+') as csvfile:
            if not sth.calibrated:
                csvfile.writelines("%s, %s" % (ntcResistance, temperature))
            else:
                csvfile.writelines("%s, %s, %s, %s, %s" (ntcResistance, temperature, sth.A, sth.B, sth.C))
