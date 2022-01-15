//Includes functions needed for connection to wifi and mqtt
#include "network.h"
//Includes functions needed for interfacing with sensors and instruments
#include "instruments.h"
//Includes functions needed for reading and writing to the file system
#include "files.h"

#define ONE_HOUR 3600000000 //One hour in microseconds

void setup() {

  //Initialize serial
  Serial.begin(115200);
  Serial.println();
  
  //Initalize file system
  init_files();

  //Grab sensor value
  float soil_temp = read_soil_temp();
  delay(1);
  
  //If a successful connection is established with the MQTT broker
  if(connect_wifi() && connect_mqtt()){

    //Pull the date from the date file
    char reading[30];
    read_date(reading);

    //Add the temp value to the string
    sprintf(reading, "%s/%.2f", reading, soil_temp);

    //Publish reading plus any readings in temp file
    publish_readings(reading);

    //If a successful connection is not established with the MQTT broker
    }else{

      //Pull the date from the date file, increment its offset, and put it back
      char reading[30];
      read_date(reading);
      increment_offset(reading);
      write_date(reading);

      //Add the temp value to the string
      sprintf(reading, "%s/%.2f", reading, soil_temp);

      //Print the reading into the temp file
      write_reading(reading);
      
      }

  //Go back to sleep
  Serial.println("Going back to sleep...");
  ESP.deepSleep(60000000); 
  delay(1000);     
  
}

void loop() {}
