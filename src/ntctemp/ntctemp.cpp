/*
ntctemp lib 0x01

copyright (c) Davide Gironi, 2017

Released under GPLv3.
Please refer to LICENSE file for licensing information.
*/

#include "ntctemp.h"

#include "math.h"

/**
 * Constructor
 */
NTCTemp::NTCTemp() {
}

/**
 * get temperature using Beta Model Equation
 * @param  adcresistence adc resistence read
 * @param  beta          beta value
 * @param  adctref       temperature reference for the measuread value
 * @param  adcrref       resistance reference for the measured value
 * @return               temperature in Celsius
 */
float NTCTemp::getB(long adcresistence, int beta, float adctref, int adcrref) {
	// use the Beta Model Equation
	// temperature (kelvin) = beta / ( beta / tref + ln ( R / rref ) )
	float t;
	t = beta / ( beta / (float)(adctref + 273.15) + log ( adcresistence / (float)adcrref ) );
	t = t - 273.15; // convert Kelvin to Celcius
	return t;
}

/**
 * Get temperature using the Steinhart-Hart Thermistor Equation
 * @param  adcresistence adc resistence read
 * @param  A             "A" equation parameter
 * @param  B             "B" equation parameter
 * @param  C             "C" equation parameter
 * @return               temperature in Celsius
 */
float NTCTemp::getSH(long adcresistence, float A, float B, float C) {
	// use the Steinhart-Hart Thermistor Equation
	// temperature (Kelvin) = 1 / (A + B*ln(R) + C*(ln(R)^3))
	float t;
	t = log(adcresistence);
	t = 1 / (A + (B * t) + (C * t * t * t));
	t = t - 273.15; // convert Kelvin to Celcius
	return t;
}

/**
 * Convert Celcius to Fahrenheit
 * @param  t celsius temperature
 * @return   temperature
 */
float NTCTemp::celsiusToFahrenheit(float t) {
	return t = (t * 9.0) / 5.0 + 32.0;
}
