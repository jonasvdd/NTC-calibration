#include <Arduino.h>

#define ANALOGPIN   A5
#define BUTTONPIN 2


void setup() {
    Serial.begin(9600);
    pinMode(ANALOGPIN, INPUT);
    pinMode (BUTTONPIN,INPUT);
    attachInterrupt(digitalPinToInterrupt(button), button, RISING);
}


void loop() {
    // Empty loop
}


void button() {
    int value = analogRead(ANALOGPIN);
    Serial.println(value);
}
