#include <Arduino.h>


void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
}


void loop() {
    // put your main code here, to run repeatedly:
    Serial.println(1000);
    delay(1000);
    Serial.println(200);
    delay(1000);
    Serial.println(612);
    delay(1000);
}