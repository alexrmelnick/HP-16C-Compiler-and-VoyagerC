#include "VoyagerC.h"

Mode mode;
uint8_t word_size;

void setMode(Mode my_mode, uint8_t my_word_size) {
    if(my_word_size > MAX_WORD_SIZE){
        printf("ERROR: Word size too large\n");
        return;
    } 
    else {
        word_size = my_word_size;
    }
    
    mode = my_mode;
}