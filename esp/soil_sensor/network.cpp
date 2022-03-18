#include <ESP8266WiFi.h> //General WiFi
#include <PubSubClient.h> //MQTT client

#include "network.h"
#include "files.h"

//Login details for the network
const char* ssid = "NAKNET2.4";
const char* password = "spongecream";

//IP addresses for the esp:
IPAddress ip(192, 168, 0, 145);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);

//Variables to define the number of miliseconds until wifi timeout
const int wifi_timeout = 15000;
//Variable to define the number of times to try a connection to the broker
const int mqtt_timeout = 3;

//Bool to store whether or not we have recieved the date
boolean date_recieved = false;

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
  while(!mqtt_client.connect("esp","esp", "bigzucchini")){ //While mqtt hasn't connected
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
  if(mqtt_client.subscribe("date/current")){

    DEBUG_SERIAL.println("Date subcription successful");
    
    }else{
      
      DEBUG_SERIAL.println("Date subcription unsuccessful");
      
      }

  //Listen for messages until the date is recieved
  while(!date_recieved){mqtt_client.loop();}

  return true;
    
  }


//Callback for when message is read
void on_message(const char topic[], byte* payload, unsigned int len){

  DEBUG_SERIAL.print("Recieved a message in: ");
  DEBUG_SERIAL.println(topic);
  //Choose logic based on the topic
  if(strcmp(topic, "date/current") == 0){

    //Convert the byte payload into a date string
    char date[len];
    for(int i = 0; i < len; i++){
      date[i] = (char)payload[i];
    }
    date[len] = '\0';

    DEBUG_SERIAL.print("Recieved current date as: ");
    DEBUG_SERIAL.println(date);

    //Write the date into the date file
    write_date(date);

    date_recieved = true;
    
    }
    
  }

//Publish a given reading to the mqtt client
void publish_reading(char reading[]){

  boolean valid = validate_reading(reading);
  
  DEBUG_SERIAL.print("Publishing reading: ");
  DEBUG_SERIAL.print(reading);
  DEBUG_SERIAL.print(" which has been validated: ");
  DEBUG_SERIAL.println(valid);

  if(valid) mqtt_client.publish("esp/sensor1", reading);
  
  }
