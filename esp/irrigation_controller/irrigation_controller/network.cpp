#include <ESP8266WiFi.h> //General WiFi
#include <PubSubClient.h> //MQTT client

#include "network.h"

//Variable to store the volume, drain, and cancel signals of the mqtt message
float recieved_volume;
float recieved_drain_pressure;
boolean recieved_cancel = false;

//Login details for the network
const char* ssid = "NAKNET2.4";
const char* password = "spongecream";

//IP addresses for the esp:
IPAddress ip(192, 168, 0, 146);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);

//Variables to define the number of miliseconds until wifi timeout
const int wifi_timeout = 15000;
//Variable to define the number of times to try a connection to the broker
const int mqtt_timeout = 3;

//WiFi client object will allow the ESP to connect as a client to the host
WiFiClient wifi_client;

//MQTT client will allow the ESP to connect to the broker
PubSubClient mqtt_client(wifi_client);

//Connect the ESP to the wifi network, return false if no connection is established
boolean connect_wifi(){

  DEBUG_SERIAL.print("MAC address: ");
  DEBUG_SERIAL.println(WiFi.macAddress());

  DEBUG_SERIAL.print("\n");
  DEBUG_SERIAL.print("Connecting to: ");
  DEBUG_SERIAL.println(ssid);

  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password); //Initialize connection

  unsigned long st = millis();

  //Loop until wifi is connected
  while(WiFi.status() != WL_CONNECTED){ //While wifi hasn't connected
    delay(500);
    if(millis() - st >= wifi_timeout){ //If connection has been tried for WiFi_timeout milliseconds
      DEBUG_SERIAL.print("\n");
      DEBUG_SERIAL.println("WiFi connection timed out");
      DEBUG_SERIAL.print("WiFi status: ");
      DEBUG_SERIAL.println(WiFi.status());
      return false;
      }
  }
  
  unsigned long elapsed = millis() - st;

  DEBUG_SERIAL.print("\n");
  DEBUG_SERIAL.print("Connected to WiFi: ");
  DEBUG_SERIAL.print(WiFi.SSID());
  DEBUG_SERIAL.print(" in: ");
  DEBUG_SERIAL.print(elapsed);
  DEBUG_SERIAL.println(" miliseconds");

  return true;
  
  }

//Connect the ESP to the MQTT broker, return false if no connection is established
boolean connect_mqtt(){

  //Add server and callback functions to mqtt client object
  mqtt_client.setServer("192.168.0.195", 1883);
  mqtt_client.setCallback(on_message);

  DEBUG_SERIAL.print("\n");
  DEBUG_SERIAL.print("Connecting to broker...");

  int count = 1;
  while(!mqtt_client.connect("irrigation_controller","irrigation_controller", "chunkybroc")){ //While mqtt hasn't connected
    DEBUG_SERIAL.print("*");
    delay(500);
    if(count == mqtt_timeout){ //If connection has been tried wifi_timeout times, return 0
      DEBUG_SERIAL.print("\n");
      DEBUG_SERIAL.println("MQTT connection timed out");
      //mqttClient.state();
      return false;
      }
    count++;
  }

  DEBUG_SERIAL.print("\n");
  DEBUG_SERIAL.println("Connected to broker");

  //Subscribe to topics
  if(mqtt_client.subscribe("irrigation/activate")){
    DEBUG_SERIAL.println("Activation subcription successful");
    }else{
      DEBUG_SERIAL.println("Activation subcription unsuccessful");
      }

  return true;
    
  }


//Callback for when message is read
void on_message(const char topic[], byte* payload, unsigned int len){

  DEBUG_SERIAL.print("Recieved a message in: ");
  DEBUG_SERIAL.println(topic);
  
  //Choose logic based on the topic
  if(strcmp(topic, "irrigation/activate") == 0){
    
    char payload_char[len];
    for(int i = 0; i < len; i++){
      payload_char[i] = (char)payload[i];
      }

    recieved_volume = atof(payload_char);
    DEBUG_SERIAL.print("Recieved volume: ");
    DEBUG_SERIAL.println(recieved_volume);
    
    }else if(strcmp(topic, "irrigation/drain") == 0){

      char payload_char[len];
      for(int i = 0; i < len; i++){
        payload_char[i] = (char)payload[i];
        }
  
      recieved_drain_pressure = atof(payload_char);
      DEBUG_SERIAL.print("Recieved drain pressure: ");
      DEBUG_SERIAL.println(recieved_drain_pressure);
      
      }else if(strcmp(topic, "irrigation/cancel") == 0){
      
        recieved_cancel = true;
      
        }
    
  }

void loop_mqtt(){
  mqtt_client.loop();
  }

void publish_json(char* json_buffer, size_t n){
  mqtt_client.publish("irrigation/report", json_buffer, n);
  }

float get_target_volume(){
  return recieved_volume;
  recieved_volume = NULL;
  }

float get_target_drain_pressure(){
  return recieved_drain_pressure;
  recieved_drain_pressure = NULL;
  }

boolean get_cancel(){
  return recieved_cancel;
  recieved_cancel = false;
  }
