#include "DS1621.h"
#include <Wire.h>

static uint8_t ds1621_write(uint8_t reg, uint8_t value) {
    Wire.beginTransmission(DS1621_ADDR);
    Wire.write(reg);
    Wire.write(value);
    return Wire.endTransmission();
}
uint8_t ds1621_begin() {
    Wire.begin();
    uint8_t err = ds1621_write(0xAC, 0x01);  
    delay(15);
    return err;
}
uint8_t ds1621_startConvert() {
    Wire.beginTransmission(DS1621_ADDR);
    Wire.write(0xEE);                       
    return Wire.endTransmission();
}
uint8_t ds1621_readTemp(float &t) {
    Wire.beginTransmission(DS1621_ADDR);
    Wire.write(0xAA);                        
    uint8_t err = Wire.endTransmission(false);  
    if (err) return err;
    if (Wire.requestFrom((uint8_t)DS1621_ADDR, (uint8_t)2) != 2) return 10;
    int8_t msb = Wire.read();                
    uint8_t lsb = Wire.read();               
    t = msb + ((lsb & 0x80) ? 0.5 : 0.0);
    return 0;
}