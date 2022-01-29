from picamera import PiCamera
from datetime import datetime
import os
import json
import requests

camera = PiCamera()

#Import photos path
dirname = os.path.dirname(__file__)
photos = os.path.join(dirname, 'photos')

#Import environment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
API_KEY = str(os.getenv('OPENWEATHERMAP_KEY'))
LAT_COORDINATE = float(os.getenv('LAT_COORDINATE'))
LONG_COORDINATE = float(os.getenv('LONG_COORDINATE'))
url = f'https://api.openweathermap.org/data/2.5/weather?lat={LAT_COORDINATE}&lon={LONG_COORDINATE}&appid={API_KEY}&units=metric'

#Takes a picture if the time is within sunrise and sunset
def cam_capture():

    #Call API
    response = requests.get(url)
    data = json.loads(response.text)

    #Pull sunrise and sunset times
    sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
    sunset = datetime.fromtimestamp(data['sys']['sunset'])

    #Take picture if time is within sunrise and sunset
    now = datetime.now()
    if now > sunrise and now < sunset:
        now = now.strftime('%Y-%m-%d-%H.png')
        file_path = os.path.join(photos, now)
        camera.capture(file_path)

