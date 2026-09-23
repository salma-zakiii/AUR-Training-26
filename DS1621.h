#ifndef DS1621_H
#define DS1621_H
#include <Arduino.h>
#define DS1621_ADDR 0x48

uint8_t ds1621_begin();                 
uint8_t ds1621_startConvert();           
uint8_t ds1621_readTemp(float &t);       

#endif