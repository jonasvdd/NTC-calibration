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

import time


#######################
#      constants
#######################
# Serial communication with the microcontroller
BAUDRATE =        9600
PORT =            '/dev/ttyUSB0'

# Measurement board dependent variables
SERIAL_RESISTOR = 47400
ACCURACY_ADC =    1023

CSV_FILE = 'data/csv_' + time.strftime("%Y-%m-%d_%H-%M") + '.csv'

if __name__ == '__main__':
    # Initialize the key objects
    tsp01 = TSP01()                         # accurate Temperature logger
    serial = ArduinoSerial(PORT, BAUDRATE)  # serial monitor to retrieve ADC value
    sth = SteinHart()                     # calculating and calibration the Steinhart-Hart equation/coefficients


    def v_devider_rntc(adc_val):
        return SERIAL_RESISTOR * (ACCURACY_ADC - adc_val) / adc_val

    while(True):
        adc_val = int(serial.readSerial())
        print("arduino serial:\t\t%s" % adc_val)

        ntcResistance = v_devider_rntc(adc_val)
        print("ntc resistance:\t\t%s ohm" % ntcResistance)
        probe_temp = tsp01.probe_1_temperature()
        print("probe temprature:\t%s °C" % probe_temp)

        # feed the data so it can be used for calibration
        sth.feed(probe_temp, ntcResistance)

        calc_temp = sth.calculateT(ntcResistance)
        print("calculated temperature:\t%s °C \n" % calc_temp)
        print(sth)
        print("-"*60)

        # Save the data in the csv
        with open(CSV_FILE, mode='a+') as csvfile:
            if not sth.calibrated:
                csvfile.writelines("%s, %s \n" % (ntcResistance, probe_temp))
            else:
                csvfile.writelines("%s, %s, %s, %s, %s, %s, %s \n" % 
                (ntcResistance, probe_temp, calc_temp, sth.A, sth.B, sth.C, sth.TR_values))