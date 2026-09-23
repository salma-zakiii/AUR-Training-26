#define F_CPU 8000000UL
#include <avr/io.h>
#include <util/delay.h>

int main(void) {
    DDRB |= (1 << PB3);  
    TCCR0 |= (1 << WGM01) | (1 << WGM00);   
    TCCR0 |= (1 << COM01);                  
    TCCR0 |= (1 << CS01);                   
    uint8_t duty = 64;  
    OCR0 = duty;

    while (1) {
        for (duty = 64; duty < 255; duty++) {
            OCR0 = duty;
            _delay_ms(10);
        }
        for (duty = 255; duty > 64; duty--) {
            OCR0 = duty;
            _delay_ms(10);
        }
    }
}