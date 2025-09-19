#ifndef _F1_H_
#define _F1_H_

#include "stdint-uintn.h" 
#include "esp_matter.h" 

esp_matter_attr_val_t my_matter_function(esp_matter_attr_val_t mav);
uint16_t my_first_function(bool b,uint8_t u8);
const uint8_t my_second_function(const uint8_t u8);

#endif // _F1_H_
