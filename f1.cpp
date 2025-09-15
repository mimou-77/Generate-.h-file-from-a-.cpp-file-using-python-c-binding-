#include "stdint-uintn.h"
#include "esp_matter.h"



//esp_matter_attr_val_t
esp_matter_attr_val_t my_matter_function(esp_matter_attr_val_t mav)
{
    return mav;
}


//bool + uint8_t
uint16_t my_first_function(bool b, uint8_t u8)
{
    uint16_t a = u8;
    return a;
}

//const
const uint8_t my_second_function(const uint8_t u8)
{
    const uint8_t a = 7;
    return a;
}
