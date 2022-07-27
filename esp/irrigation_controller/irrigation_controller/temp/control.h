#ifndef CONTROL_H
#define CONTROL_H

#define DEBUG false  //set to true for debug output, false for no debug output
#define DEBUG_SERIAL if(DEBUG)Serial

void dispense_volume(float target_volume);

#endif
