#include <ArduinoJson.h>

#define FLOW_SENSOR 5
#define BARREL_VALVE 12
#define HOSE_VALVE 13
#define DRAIN_VALVE 14

//Functions for connecting to WiFi and MQTT
#include "network.h"
//Functions for fluid control
//#include "control.h"

#define DEBUG true  //set to true for debug output, false for no debug output
#define DEBUG_SERIAL if(DEBUG)Serial

//This is the amount of pulses returned by the sensor per liter, calibrated through testing
#define PPL 1265.289

//Stores how long to wait for barrel's water to reach flow meter
unsigned int barrel_timeout = 5000;

//When dispensing water, define what litre resolution to save snapshots of data
const float data_resolution = 0.2;

//This integer needs to be set as volatile to ensure it updates correctly during the interrupt process.
volatile int pulses = 0; 

float target_volume = NULL;
float target_drain_pressure = NULL;
boolean cancel = false;

//Every time the flow sensor sends a pulse, increment the pulse count
ICACHE_RAM_ATTR void Flow(){
   pulses++;
}

void setup() {

  //Configure pin modes
  pinMode(FLOW_SENSOR, INPUT_PULLUP);
  pinMode(BARREL_VALVE, OUTPUT);
  pinMode(HOSE_VALVE, OUTPUT);
  pinMode(DRAIN_VALVE, OUTPUT);
  digitalWrite(BARREL_VALVE, LOW);
  digitalWrite(HOSE_VALVE, LOW);
  digitalWrite(DRAIN_VALVE, LOW);

  //Attach the Flow() interrupt function to the flow sensor pin
  attachInterrupt(digitalPinToInterrupt(FLOW_SENSOR), Flow, RISING);

  //Initialize serial
  DEBUG_SERIAL.begin(115200);

  //Connect to WiFi and MQTT broker
  connect_wifi();
  connect_mqtt();
  
}

void loop() {

  loop_mqtt();

  //If drain pressure has changed, meaning an activation signal has been recieved
  target_drain_pressure = get_target_drain_pressure();
  if(target_drain_pressure) {
    drain_pressure(target_drain_pressure);
    }

  //If target volume has changed, meaning an activation signal has been recieved
  target_volume = get_target_volume();
  if(target_volume) {
    dispense_volume(target_volume);
    ESP.restart();
    }

  delay(50);
  
}

void drain_pressure(float target_drain_pressure){

  DEBUG_SERIAL.print("Draining barrel to: ");
  DEBUG_SERIAL.println(target_drain_pressure);

  digitalWrite(DRAIN_VALVE, HIGH);

  while(true){

    float pressure = get_pressure();

    if(pressure <= target_drain_pressure){

      digitalWrite(DRAIN_VALVE, LOW);
      DEBUG_SERIAL.print("Barrel drained to: ");
      DEBUG_SERIAL.println(pressure);
      break;
      
      }
    
    }
  
  }

float get_pressure(){
  
  return 101.3;
  
  }

void dispense_volume(float target_volume){

  DynamicJsonDocument doc(2048);

  //Volume, time, rate, barrel_flag, hose_flag

  pulses = 0;
  float volume = 0;
  float last_volume = 0;
  float barrel_volume = 0;
  int last_pulses = 0;
  float rate = 0;
  float avg_rate;
  float avg_count = 0;
  float pressure;
  unsigned long int last_timestamp = millis();
  unsigned long int barrel_start_timestamp; //Store timestamp of barrel opening
  unsigned long int barrel_off_timestamp = NULL;

  bool barrel_flag = true;
  bool hose_flag = false;

  digitalWrite(BARREL_VALVE, HIGH);
  digitalWrite(HOSE_VALVE, LOW);
  barrel_start_timestamp = millis();

  int count = 0;

  while(true){

    loop_mqtt();
    cancel = get_cancel();
    if(cancel){
      ESP.restart();      
      }

    //Total volume is the total amount of pulses divided by the amount of pulses per liter
    volume = (pulses / PPL);

    //Flow rate is the amount of pulses in the last tick divided by the time elapsed since the last tick in Liters/min
    if(pulses > 0){
      rate = (((pulses - last_pulses) / PPL) / (millis() - last_timestamp)) * 1000 * 60;
      last_pulses = pulses;
      last_timestamp = millis();
      }

    //Update rate count for reporting in json
    avg_rate += rate;
    avg_count++;
    pressure = 101.3;

    DEBUG_SERIAL.print("Volume: ");
    DEBUG_SERIAL.print(volume);
    DEBUG_SERIAL.print(", Rate(L/min): ");
    DEBUG_SERIAL.println(rate);


    //When change in volume equals data resolution, save snapshot to json
    if((volume - last_volume) >= data_resolution){

      avg_rate /= avg_count;

      doc["time"][count] = millis() - barrel_start_timestamp;
      doc["volume"][count] = (int)(volume * 1000);
      doc["avg_rate"][count] = (int)(avg_rate * 1000);
      doc["avg_pressure"][count] = (int)pressure;
      
      avg_rate = 0;
      avg_count = 0;
      count++;
      last_volume = volume;
      }

    //Break once target volume has been reached
    if(volume >= target_volume){

      //If the dispensing process is ended without switching to the hose, set the barrel volume to the volume
      if(barrel_flag && !hose_flag){
        barrel_volume = volume;        
        }

      avg_rate /= avg_count;

      digitalWrite(BARREL_VALVE, LOW);
      digitalWrite(HOSE_VALVE, LOW);

      DEBUG_SERIAL.print("Deactivated. Final volume: ");
      DEBUG_SERIAL.println(volume);

      doc["time"][count] = millis() - barrel_start_timestamp;
      doc["volume"][count] = (int)(volume * 1000);
      doc["avg_rate"][count] = (int)(rate * 1000);
      doc["avg_pressure"][count] = (int)pressure;;

      doc["barrel_volume"] = (int)(barrel_volume * 1000);
      doc["barrel_off_timestamp"] = barrel_off_timestamp - barrel_start_timestamp;

      char json_buffer[256];
      size_t n = serializeJson(doc, json_buffer);
      publish_json(json_buffer, n);
      
      break;
      
      }

    //Switch to hose once barrel is expended
    if(rate <= 0.3 && ((millis() - barrel_start_timestamp) > barrel_timeout) && barrel_flag && !hose_flag){

      barrel_volume = volume;
      barrel_flag = false;
      hose_flag = true;
      barrel_off_timestamp = millis();
      digitalWrite(BARREL_VALVE, LOW);
      delay(50);
      digitalWrite(HOSE_VALVE, HIGH);

      DEBUG_SERIAL.println("Barrel expended. Hose activated");
      
      } 

    delay(50);

    }
  
  }
