import numpy as np
import select

from Arduino import Arduino
from TSP01 import TSP01

def v_devider_rntc(a2dval):
    


if __name__ == '__main__':
    # constants
    BAUDRATE = 9600
    PORT = '/dev/ttyUSB1'
    CSVFILE = 'calibrationdata.csv'

    SERIALRESISTOR = '47400'
    VARDUINO = 5
    ACCURACYARDUINO = 1023

    tsp01 = TSP01()
    arduino = Arduino(PORT, BAUDRATE)

    for i in range(3):
        adval = arduino.readSerial()
        print("arduino serial: ", int(adval))
        Vntc = VARDUINO * int(adval) / ACCURACYARDUINO  # voltage over 
        print("vntc: ", Vntc)
        ntcResistance =  Vntc / ( VARDUINO - Vntc) * SERIALRESISTOR

        print("ntc resistance: %s ohm" % ntcResistance)
        
        temperature = tsp01.probe_1_temperature()

        with open(CSVFILE, mode='a+') as csvfile:
            csvfile.writelines("%s, %s\n" % (ntcResistance, temperature))
