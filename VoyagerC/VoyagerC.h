#ifndef VOYAGER_C_H
#define VOYAGER_C_H

#include <stdio.h>
#include <math.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

uint8_t word_size;
#define MAX_WORD_SIZE 64

typedef enum {
    MODE_1C,
    MODE_2C,
    MODE_U
} Mode;

void hp16c_setMode(Mode my_mode, uint8_t my_word_size);

#endif // VOYAGER_C_H