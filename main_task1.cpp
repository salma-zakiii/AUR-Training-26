#define F_CPU 8000000UL
#include <avr/io.h>

int main(void) {
    DDRB |= (1 << PB0);              

    TCCR0 |= (1 << WGM01);             
    TCCR0 |= (1 << CS01) | (1 << CS00); 
    OCR0 = 124;                        
    uint16_t ms_count = 0;
    while (1) {
        if (TIFR & (1 << OCF0)) {
            TIFR |= (1 << OCF0);    
            ms_count++;
            if (ms_count >= 500) {
                PORTB ^= (1 << PB0); 
                ms_count = 0;
            }
        }
    }
}