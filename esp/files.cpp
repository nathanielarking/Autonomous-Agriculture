#include <FS.h> //File system

#include "files.h"
#include "network.h"

//Initialize file system
void init_files(){

    //Turn off autoformatting just in case
    SPIFFSConfig cfg;
    cfg.setAutoFormat(true);
    SPIFFS.setConfig(cfg);

    //Initialize file system. If this fails we can't store data so restart
    if(!SPIFFS.begin()){
        Serial.println("File system failed to mount");
        ESP.restart();
        }

}

//Writes the given date to the date file
void write_date(const char date[]){

  Serial.print("Printing date: ");
  Serial.print(date);
  Serial.println(" in /date.txt");
  
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

  Serial.print("Printing reading: ");
  Serial.print(reading);
  Serial.println(" in /temp.txt");

  File temp_file = SPIFFS.open("/temp.txt", "a");
  temp_file.print(reading);
  temp_file.print(',');
  temp_file.close();
  
  }

//Push all readings from temp file into mqtt, in addition to the reading passed as an argument
void publish_readings(char last_reading[]){
  
  File temp_file = SPIFFS.open("/temp.txt", "r");
  char reading[30];

  //Loop through temp file and read every line into the buffer, then publish it.
  while(temp_file.available()){
    int len = temp_file.readBytesUntil(',', reading, sizeof(reading)-1);
    reading[len] = '\0';
    publish_reading(reading);
    delay(10);
    }

  //Publish the remaining reading
  publish_reading(last_reading);

  //Remove temp file so we don't store more values than needed on the ESP
  temp_file.close();
  SPIFFS.remove("/temp.txt");
  
  }
