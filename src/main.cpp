#include <Arduino.h>

//include main
#include "main.h"

//include ADS1015 library
#include <Adafruit_ADS1015.h>
//contruct ADS1015
Adafruit_ADS1015 ads;

//include ADS1x15Helper library
#include "ads1x15helper/ads1x15helper.h"
//contruct ADS1x15Helper
ADS1x15Helper adshelper;

//include NTCTemp library
#include "ntctemp/ntctemp.h"
//contruct NTCTemp
NTCTemp ntc;

//ADS gain
#define ADS_GAIN GAIN_ONE
//ADSHelper mode
#define ADSHELPER_ADS ADS1X15HELPER_ADS1015
//ADSHelper gain
#define ADSHELPER_GAIN ADS1X15HELPER_GAIN_ONE

/**
 * Main setup
 */
void setup(void) {
  //initialize Serial
  Serial.begin(115200);
  delay(500);
  Serial.println("Starting...");

  //initialize ADS
  ads.setGain(ADS_GAIN);
  ads.begin();

  //initialize ADSHelper
  adshelper.setStepVoltage(ADSHELPER_ADS, ADSHELPER_GAIN);
}

/**
 * Main loop
 */
void loop(void) {
  uint16_t adcraw = ads.readADC_SingleEnded(0); delay(7);
  float vol = adshelper.adcToVoltage(adcraw);
  uint32_t res = adshelper.adcToResistence(adcraw, 22000, 3.3f);
  float tempB = ntc.getB(res, 3470, 25, 10000);
  float tempSH = ntc.getSH(res, (float)0.947070725e-3, (float)2.450662058e-4, (float)1.853992838e-7);
  Serial.print("ADC        : "); Serial.println(adcraw);
  Serial.print("Voltage    : "); Serial.println(vol);
  Serial.print("Resistance : "); Serial.println(res);
  Serial.print("Temp B     : "); Serial.println(tempB);
  Serial.print("Temp SH    : "); Serial.println(tempSH);
  Serial.println(" ");

  delay(1000);
}
