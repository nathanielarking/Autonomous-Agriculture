#ifndef INSTRUMENTS_H
#define INSTRUMENTS_H

#define DEBUG false  //set to true for debug output, false for no debug output
#define DEBUG_SERIAL if(DEBUG)Serial

//Returns the floating point soil temperature value
float read_soil_temp();

#endif
