#ifndef NETWORK_H
#define NETWORK_H

#define DEBUG true  //set to true for debug output, false for no debug output
#define DEBUG_SERIAL if(DEBUG)Serial

//Connect to wifi, timeout after a certain number of tries
bool connect_wifi();

//Connect to mqtt, timeout after a certain number of tries
bool connect_mqtt();

//Callback for when message is read
void on_message(const char* topic, byte* payload, unsigned int length);

//Allow the MQTT to update
void loop_mqtt();

//Publish the json from the dispensing process
void publish_json(char* json_buffer, size_t n);

//Returns the target volume as collected from the MQTT server
float get_target_volume();

//Returns the target drain pressure as collected from the MQTT server
float get_target_drain_pressure();

//Returns the cancel signal as collected from the MQTT server
boolean get_cancel();

#endif
