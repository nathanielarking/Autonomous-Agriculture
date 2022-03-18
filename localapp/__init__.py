from data import engine, init_engine
from . import mqtt

#Allow the thread to restart after any interruptions
def localapp_thread():
    while True:
        try:
            run_localapp()
        except BaseException as e:
            print('{!r}; restarting thread'.format(e))

def run_localapp():

    init_engine()

    #Uncomment this code to utilize the functions which import data from csv files into the database (may not work for your files)
    #from data.interface import csv_to_sql, csv_to_sql_harvest_data, csv_to_sql_temp_data, update_temp_file, csv_to_sql_harvest_data
    #Add plant attributes into database
    #csv_to_sql()
    #Add sensor data into database and update file table
    #csv_to_sql_temp_data()
    #update_temp_file()
    #csv_to_sql_harvest_data()

    #Initialize our mqtt client
    client = mqtt.connect()

    #Subscribe client to relevant topics
    mqtt.subscribe(client)

    #Tell the client to listen 
    mqtt.update(client)