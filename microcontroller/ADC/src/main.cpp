#include <Arduino.h>

#define ANALOGPIN   A5
#define BUTTONPIN 2

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers


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
    if ((millis() - lastDebounceTime) > debounceDelay) {
        lastDebounceTime = millis();
        int value = analogRead(ANALOGPIN);
        Serial.println(value);
    }
}
