#include <Arduino.h>

#define ANALOGPIN   A0

void setup() {
    Serial.begin(9600);
}


void loop() {
    int value = analogRead(ANALOGPIN);
    Serial.println(value);
    delay(1000);
    Serial.println(200);
    delay(1000);
    Serial.println(612);
    delay(1000);
}