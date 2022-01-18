#include <FS.h> //File system

#include "files.h"
#include "network.h"

//Initialize file system
void init_files(){

    //Turn off autoformatting just in case
    SPIFFSConfig cfg;
    cfg.setAutoFormat(false);
    SPIFFS.setConfig(cfg);

    //Initialize file system. If this fails we can't store data so restart
    if(!SPIFFS.begin()){
        DEBUG_SERIAL.println("File system failed to mount");
        ESP.restart();
        }

}

//Writes the given date to the date file
void write_date(const char date[]){

  DEBUG_SERIAL.print("Printing date: ");
  DEBUG_SERIAL.print(date);
  DEBUG_SERIAL.println(" in /date.txt");
  
  File date_file = SPIFFS.open("/date.txt", "w");
  date_file.print(date);
  date_file.close();

}

//Reads from the date file into a char array
void read_date(char date[]){

  File date_file = SPIFFS.open("/date.txt", "r");

  int i = 0;
  while(date_file.available()){
    date[i++] = date_file.read();
    }
    date[i] = '\0';

  date_file.close();

}

//Takes in a date char array and increments the offset by 1
void increment_offset(char date[]){

  char offset[5];
  int i = 0;

  //Move index to end of date
  while(date[i] != '\0'){i++;}

  //Move index to beginning of offset
  while(date[i] != '/'){i--;}
  i++;
  int truncate = i; //Save position for truncation later

  //Copy offset into seperate char array
  int j = 0;
  while(date[i] != '\0'){
    offset[j] = date[i];
    j++;
    i++;
    }
    offset[j] = '\0';

  //Truncate original date string so it can be re-formatted
  date[truncate] = '\0';

  //Convert offset into integer
  int offset_int = atoi(offset);

  //Put offset back into date array while incrementing offset
  sprintf(date, "%s%d", date, ++offset_int);

}

//Writes temp reading to temp file
void write_reading(char reading[]){

  boolean valid = validate_reading(reading);

  DEBUG_SERIAL.print("Printing reading: ");
  DEBUG_SERIAL.print(reading);
  DEBUG_SERIAL.print(" which has been validated: ");
  DEBUG_SERIAL.print(valid);
  DEBUG_SERIAL.println(" in /temp.txt");

  if(valid){
    
    File temp_file = SPIFFS.open("/temps.txt", "a");
    temp_file.print(reading);
    delay(250);
    temp_file.print(',');
    temp_file.close();
    }
  
  }

//Push all readings from temp file into mqtt, in addition to the reading passed as an argument
void publish_readings(char last_reading[]){
  
  File temp_file = SPIFFS.open("/temps.txt", "r");
  char reading[30];

  //Loop through temp file and read every line into the buffer, then publish it.
  if(temp_file){
    while(temp_file.available()){
      int len = temp_file.readBytesUntil(',', reading, sizeof(reading)-1);
      reading[len] = '\0';
      publish_reading(reading);
      delay(50);
      }
    }

  //Publish the remaining reading
  publish_reading(last_reading);

  //Remove temp file so we don't store more values than needed on the ESP
  temp_file.close();
  SPIFFS.remove("/temps.txt");
  
  }

//Make sure that the data we have read is valid, and doesn't contain any characters that aren't supposed to be there
boolean validate_reading(char reading[]){

  //Only return true if all values are either '-', '/', ',' or '0' to '9' and only if the reading contains the correct amount of delimeters
  int i = 0;
  int count = 0;
  while(reading[i] != '\0'){
    if(reading[i] == '/') count++;
    if(reading[i] < '-' || reading[i++] > '9') return false;
    } 
      
  if(count == 5) return true;
  return false;
  
  }
