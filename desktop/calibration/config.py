# -*- coding: utf-8 -*-
"""
    **********
    config.py
    **********
    
    Withholds global configurations
"""
__author__ = 'Jonas Van Der Donckt'


#######################
#      constants
#######################
# Serial communication with the microcontroller
BAUDRATE =        9600
PORT =            '/dev/ttyUSB0'

# Measurement board dependent variables
SERIAL_RESISTOR = 47550 # fluke 45
ACCURACY_ADC =    1023

#######################
#     Methods
#######################
def v_devider_rntc_adc_r(adc_const_r):
    """
    Circuit::

            VCC
             ┬
             │
             ▒ R_NTC
             │
             ├──────────── --> Goes to microcontroller
             │
             █ R_const
             │
             ┴
            GND

    :param int adc_const_r: Analog to digital converted value
    :return: Resistance of the NTC resistor (ohm)
    :rtype: float
    """
    return SERIAL_RESISTOR * (ACCURACY_ADC - adc_const_r) / adc_const_r


def v_devider_rntc_adc_ntc(adc_ntc):
    """
    Circuit::

            VCC
             ┬
             │
             █ R_const
             │
             ├──────────── --> Goes to microcontroller
             │
             ▒ R_NTC
             │
             ┴
            GND 

    :param int adc_const_r: The analog to digital converted value
    :return: Resistance of the NTC resistor (ohm)
    :rtype: float
    """
    return SERIAL_RESISTOR * adc_ntc / (ACCURACY_ADC - adc_ntc)


def calc_Rntc(adc):
    """
    Calculates the resistance of the NTC resistor, based
    on the ADC digital value of the microcontroller.

    .. NOTE::

        If you use another circuit, just change the method to you
        correspondign calculations
             
    :param int adc: The analog to digital converted value
    :return: The Resistance of the NTC resistor (ohm)
     """
    return v_devider_rntc_adc_r(adc)
