/*
ntctemp lib 0x01

copyright (c) Davide Gironi, 2017

Released under GPLv3.
Please refer to LICENSE file for licensing information.
*/

#ifndef NTCTEMP_H
#define NTCTEMP_H

#define NTCTEMP_LOOKUPRETERROR -32767

class NTCTemp {
  public:
    NTCTemp();
    float getB(long adcresistence, int beta, float adctref, int adcrref);
    float getSH(long adcresistence, float A, float B, float C);
    float celsiusToFahrenheit(float t);
};

#endif
