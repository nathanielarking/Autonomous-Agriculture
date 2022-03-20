#ifndef INSTRUMENTS_H
#define INSTRUMENTS_H

#define DEBUG false  //set to true for debug output, false for no debug output
#define DEBUG_SERIAL if(DEBUG)Serial

//Returns the floating point soil temperature value
float read_soil_temp();

//Returns the integer value for soil moisture (200-2000)
unsigned int read_soil_moisture();

#endif
