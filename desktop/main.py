# -*- coding: utf-8 -*-
"""
    *********
    main.py
    *********
    
    This script starts the application.
    It must be ran as root! 
    It will:
    * Request the user to choose the serial connection of the TSP01
    * 
    
"""
__author__ = 'Jonas Van Der Donckt'

from SteinhartHart import SteinHart
from Arduino import ArduinoSerial
from TSP01 import TSP01
from config import * 

import time




CSV_FILE = 'data/csv_' + time.strftime("%Y-%m-%d_%H-%M") + '.csv'

if __name__ == '__main__':
    # Initialize the key objects
    tsp01 = TSP01()                             # accurate Temperature logger
    serial = ArduinoSerial(PORT, BAUDRATE)      # serial monitor to retrieve ADC value
    sth = SteinHart()                           # calculating and calibration the Steinhart-Hart equation/coefficients

    while(True):
        adc_val = int(serial.readSerial())
        ntcResistance = calc_Rntc(adc_val)
        probe_temp = tsp01.probe_1_temperature()

        print("arduino serial:\t\t%s" % adc_val)
        print("ntc resistance:\t\t%s ohm" % ntcResistance)
        print("probe temprature:\t%s °C" % probe_temp)

        # feed the data so it can be used for calibration
        sth.feed(probe_temp, ntcResistance)
        calc_temp = sth.calculateT(ntcResistance)

        print("calculated temperature:\t%s °C\n" % calc_temp)
        print(sth)
        print("-"*60)

        # Save the data in the csv
        with open(CSV_FILE, mode='a+') as csvfile:
            if not sth.calibrated:
                csvfile.writelines("%s, %s \n" % (ntcResistance, probe_temp))
            else:
                csvfile.writelines("%s, %s, %s, %s, %s, %s, %s \n" % 
                (ntcResistance, probe_temp, calc_temp, sth.A, sth.B, sth.C, sth.TR_values))