#include <Arduino.h>
#include "DS1621.h"

void setup() {
    Serial.begin(9600);
    uint8_t err = ds1621_begin();
    if (err) {
        Serial.print(F("Config error: "));
        Serial.println(err);
    }
}
void loop() {
    uint8_t err = ds1621_startConvert();
    if (err) {
        Serial.print(F("Start error: "));
        Serial.println(err);
        delay(1000);
        return;
    }
    delay(800);  
    float t;
    err = ds1621_readTemp(t);
    if (err) {
        Serial.print(F("Read error: "));
        Serial.println(err);
    } else {
        Serial.print(F("Temperature: "));
        Serial.print(t, 1);
        Serial.println(F(" C"));
    }
    delay(1000);
}