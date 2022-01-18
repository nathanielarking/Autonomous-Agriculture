#ifndef NETWORK_H
#define NETWORK_H

#define DEBUG true  //set to true for debug output, false for no debug output
#define DEBUG_SERIAL if(DEBUG)Serial

//Connect to wifi, timeout after a certain number of tries
boolean connect_wifi();

//Connect to mqtt, timeout after a certain number of tries
boolean connect_mqtt();

//Callback for when message is read
void on_message(const char* topic, byte* payload, unsigned int length);

//Publish a given reading to the mqtt client
void publish_reading(char reading[]);

#endif
