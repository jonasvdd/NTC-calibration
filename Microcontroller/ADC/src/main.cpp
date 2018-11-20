#include <Arduino.h>

#define ANALOGPIN   A5

void setup() {
    Serial.begin(9600);
    pinMode(ANALOGPIN, INPUT);
}


void loop() {
    int value = analogRead(ANALOGPIN);
    Serial.println(value);
    //  delay(2000);
}