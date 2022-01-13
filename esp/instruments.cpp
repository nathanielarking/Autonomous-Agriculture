#include <OneWire.h> //Temp sensor
#include <DallasTemperature.h> //Temp sensor

#include "instruments.h"

#define SENSOR_PIN 5 //Temp sensor connected on pin GPIO5

OneWire oneWire(SENSOR_PIN); //Connect a wire object to the sensor
DallasTemperature soil_temp_sensor(&oneWire); //Connect a DallasTemperature object to read from the sensor

//Returns the floating point soil temperature value
float read_soil_temp(){

    soil_temp_sensor.begin(); //Initialize sensor
  
    soil_temp_sensor.requestTemperatures();
    return soil_temp_sensor.getTempCByIndex(0);
    
  }
