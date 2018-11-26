#######################
#      constants
#######################
# Serial communication with the microcontroller
BAUDRATE =        9600
PORT =            '/dev/ttyUSB0'

# Measurement board dependent variables
SERIAL_RESISTOR = 47400
ACCURACY_ADC =    1023

#######################
#     Methods
#######################
def v_devider_rntc_adc_r(adc_const_r):
        return SERIAL_RESISTOR * (ACCURACY_ADC - adc_const_r) / adc_const_r

def v_devider_rntc_adc_ntc(adc_ntc):
        return SERIAL_RESISTOR * adc_ntc / (ACCURACY_ADC - adc_ntc)

def calc_Rntc(adc):
    return v_devider_rntc_adc_r(adc)