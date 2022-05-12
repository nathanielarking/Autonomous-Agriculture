#include <OneWire.h> //Temp sensor
#include <DallasTemperature.h> //Temp sensor
#include "Adafruit_seesaw.h" //Moisture sensor

#include "instruments.h"

#define TEMP_SENSOR_PIN 12 //Temp sensor connected on pin GPIO12

OneWire oneWire(TEMP_SENSOR_PIN); //Connect a wire object to the sensor
DallasTemperature soil_temp_sensor(&oneWire); //Connect a DallasTemperature object to read from the sensor

Adafruit_seesaw soil_moisture_sensor;

//Returns the floating point soil temperature value
float read_soil_temp(){

    soil_temp_sensor.begin(); //Initialize sensor
  
    soil_temp_sensor.requestTemperatures();
    float temp = soil_temp_sensor.getTempCByIndex(0);

    //Sometimes the sensor gives a bad value of -127, so loop call the sensor to prevent this
    while(temp < -100 && temp > 50){
      delay(500);
      temp = soil_temp_sensor.getTempCByIndex(0);
      }

    return temp;
    
  }

//Returns the integer value for soil moisture (200-2000)
unsigned int read_soil_moisture(){
  
  int count = 0;
  while(!soil_moisture_sensor.begin(0x36)){
    
    DEBUG_SERIAL.println("Error! Soil moisture sensor not found");

    //Timeout if sensor can't connect after 3 tries
    if(count++ >= 3) return NULL;
    delay(100);
    
    }

  //Once sensor has connected, read and return value
  unsigned int moisture = soil_moisture_sensor.touchRead(0);
  DEBUG_SERIAL.print("Moisture reading: ");
  DEBUG_SERIAL.println(moisture);
  return moisture;
  
  }
