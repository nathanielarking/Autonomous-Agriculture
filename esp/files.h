#ifndef FILES_H
#define FILES_H

//Initialize file system
void init_files();

//Writes the given date to the date file
void write_date(const char date[]);

//Reads from the date file into a char array
void read_date(char date[]);

//Takes in a date char array and increments the offset by 1
void increment_offset(char date[]);

//Writes temp reading to temp file
void write_reading(char reading[]);

//Push all readings from temp file into mqtt, in addition to the reading passed as an argument
void publish_readings(char last_reading[]);

#endif
