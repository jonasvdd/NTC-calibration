/*
ADS1x15Helper lib 0x01

copyright (c) Davide Gironi, 2017

Released under GPLv3.
Please refer to LICENSE file for licensing information.
*/

#include "ads1x15helper.h"

/**
 * Constructor
 */
ADS1x15Helper::ADS1x15Helper() {
}

/**
 * Convert an adc value to a voltage value
 * @param  adcread read ADC raw value
 * @return         voltage value
 */
float ADS1x15Helper::adcToVoltage(uint16_t adcread) {
	return (float)adcread*_stepvoltage;
}

/**
 * Convert an adc value to a resistence value
 * @param  adcread            read ADC raw value
 * @param  adcbalanceresistor balance resistor
 * @param  pullupvoltage      pullup voltage
 * @return                    resistance value
 */
uint32_t ADS1x15Helper::adcToResistence(uint16_t adcread, uint32_t adcbalanceresistor, float pullupvoltage) {
  float vol = adcToVoltage(adcread);
  return (pullupvoltage-vol == 0 ? 0 : (uint32_t)(vol*(float)adcbalanceresistor)/(pullupvoltage-vol));
}


/**
 * Set the step voltage
 * @param adsmodel ADS model set ADS1X15HELPER_ADS1015, or ADS1X15HELPER_ADS1115
 * @param gain     ADS gain
 */
void ADS1x15Helper::setStepVoltage(uint8_t adsmodel, uint16_t gain) {
  if (adsmodel == ADS1X15HELPER_ADS1015) {
    if (gain == ADS1X15HELPER_GAIN_TWOTHIRDS)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_TWOTHIRDS;
    else if (gain == ADS1X15HELPER_GAIN_ONE)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_ONE;
    else if (gain == ADS1X15HELPER_GAIN_TWO)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_TWO;
    else if (gain == ADS1X15HELPER_GAIN_FOUR)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_FOUR;
    else if (gain == ADS1X15HELPER_GAIN_EIGHT)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_EIGHT;
    else if (gain == ADS1X15HELPER_GAIN_SIXTEEN)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_SIXTEEN;
  } else if(adsmodel == ADS1X15HELPER_ADS1115) {
    if (gain == ADS1X15HELPER_GAIN_TWOTHIRDS)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_TWOTHIRDS;
    else if (gain == ADS1X15HELPER_GAIN_ONE)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_ONE;
    else if (gain == ADS1X15HELPER_GAIN_TWO)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_TWO;
    else if (gain == ADS1X15HELPER_GAIN_FOUR)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_FOUR;
    else if (gain == ADS1X15HELPER_GAIN_EIGHT)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_EIGHT;
    else if (gain == ADS1X15HELPER_GAIN_SIXTEEN)
      _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_SIXTEEN;
  }
}
