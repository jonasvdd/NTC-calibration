/*
adchelper lib 0x01

copyright (c) Davide Gironi, 2017

Released under GPLv3.
Please refer to LICENSE file for licensing information.
*/

#include <Arduino.h>

#ifndef ADS1X15HELPER_H_
#define ADS1X15HELPER_H_

//defines ADS model used
#define ADS1X15HELPER_ADS1015 1
#define ADS1X15HELPER_ADS1115 2

//defines ADS gain
#define ADS1X15HELPER_GAIN_TWOTHIRDS (0x0000)
#define ADS1X15HELPER_GAIN_ONE (0x0200)
#define ADS1X15HELPER_GAIN_TWO (0x0400)
#define ADS1X15HELPER_GAIN_FOUR (0x0600)
#define ADS1X15HELPER_GAIN_EIGHT (0x0800)
#define ADS1X15HELPER_GAIN_SIXTEEN (0x0A00)

//defines voltage per step for ADS1015
#define ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_TWOTHIRDS 0.003f      // 2/3x gain +/- 6.144V  1 bit = 3mV
#define ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_ONE 0.002f            // 1x gain   +/- 4.096V  1 bit = 2mV
#define ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_TWO 0.001f            // 2x gain   +/- 2.048V  1 bit = 1mV
#define ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_FOUR 0.0005f          // 4x gain   +/- 1.024V  1 bit = 0.5mV
#define ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_EIGHT 0.00025f        // 8x gain   +/- 0.512V  1 bit = 0.25mV
#define ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_SIXTEEN 0.000125f     // 16x gain  +/- 0.256V  1 bit = 0.125mV

//defines voltage per step for ADS1115
#define ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_TWOTHIRDS 0.0001875f  // 2/3x gain +/- 6.144V  1 bit = 0.1875mV
#define ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_ONE 0.000125f         // 1x gain   +/- 4.096V  1 bit = 0.125mV
#define ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_TWO 0.0000625f        // 2x gain   +/- 2.048V  1 bit = 0.0625mV
#define ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_FOUR 0.00003125f      // 4x gain   +/- 1.024V  1 bit = 0.03125mV
#define ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_EIGHT 0.000015625f    // 8x gain   +/- 0.512V  1 bit = 0.015625mV
#define ADS1X15HELPER_STEPVOLTAGEADS1115_GAIN_SIXTEEN 0.0000078125f // 16x gain  +/- 0.256V  1 bit = 0.0078125mV

class ADS1x15Helper {
  public:
    ADS1x15Helper();
    float adcToVoltage(uint16_t adcread);
    uint32_t adcToResistence(uint16_t adcread, uint32_t adcbalanceresistor, float pullupvoltage);
    void setStepVoltage(uint8_t adsmodel, uint16_t gain);
  private:
    float _stepvoltage = ADS1X15HELPER_STEPVOLTAGEADS1015_GAIN_TWOTHIRDS;
};

#endif
