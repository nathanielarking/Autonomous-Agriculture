import paho.mqtt.client as mqtt_client
from datetime import datetime, timedelta
import logging
from data import engine
from data.models import TempReading
from sqlalchemy.orm import Session
from .camera import cam_capture


#Connection info for our mqtt client
broker = '127.0.0.1'
port = 1883

#Variable to store current date and whether this is the first run or not
current_datetime = None

def connect():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_disconnect(client, userdata, rc=0):
        logging.debug(f"Disconnected result code  {str(rc)}")
        client.loop_stop()


    # Set Connecting Client ID
    client = mqtt_client.Client('pi')
    client.username_pw_set('pi', 'largetomato')
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker, port)

    return client

#Subcribe to relevant topics and set callback for message
def subscribe(client):
    def on_message(client, userdata, msg):

        if msg.topic == 'esp/sensor1':
            #Get reading and strip unnecceary characters
            reading = str(msg.payload)
            reading = reading.strip('b\'')
            readings = reading.split('/')
            print(f"Received `{reading}` from `{msg.topic}` topic")
            
            #Grab values from reading
            year = int(readings[0])
            month = int(readings[1])
            day = int(readings[2])
            hour = int(readings[3])
            offset = int(readings[4])
            temp = float(readings[5])

            #Create date from values
            timestamp = datetime(year, month, day) + timedelta(hours=hour+offset)

            with Session(engine) as session:
                new_reading = TempReading(group='soil', datetime=timestamp, value=temp)
                session.add(new_reading)
                session.commit()
            
    client.subscribe('esp/sensor1')
    client.on_message = on_message

def publish_date(client):
    global current_datetime

    #If the hour has changed or if the date hasn't been set yet, update date and publish it
    if current_datetime is None or datetime.now().hour != current_datetime.hour:
        current_datetime = datetime.now()

        #OS dependent datetime formatting
        try:
            return_datetime = current_datetime.strftime('%Y/%-m/%-d/%-H/0')
        except ValueError:
            return_datetime = current_datetime.strftime('%Y/%#m/%#d/%#H/0')

        client.publish("date/current", return_datetime, retain=True)

        #Also, take a picture
        cam_capture()

def update(client):

    #Start a thread to check for messages
    client.loop_start()

    #Send out the date when needed
    while(True):
        publish_date(client)
