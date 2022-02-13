import os
import pandas as pd
from sqlalchemy.orm import Session, sessionmaker
from .models import Plant, TempReading, TempFile, HarvestEntry
import logging
from datetime import date
import json

from . import engine

dirname = os.path.dirname(__file__)
attributes_path = os.path.join(dirname, 'plant_attributes.csv')
temps_path = os.path.join(dirname, 'allData.csv')
harvest_path = os.path.join(dirname, 'harvest_data.csv')
frost_path = os.path.join(dirname, 'frost_dates.json')

#This file updates the TempFile table with all the new values from the TempReading table
def update_temp_file():

    #Begin session
    with Session(engine) as session:
        #Variable to store the files that were changed
        files = []
        #For every temperature reading that has not been assigned to a temp file
        for reading in session.query(TempReading).filter_by(TempFile=None):

            #Get the temp file corresponding to the date of the reading, create it if it does not exist
            date = reading.datetime.date()
            file = session.query(TempFile).filter_by(date=date).first()
            if not file:
                new_file = TempFile(date=date, group=reading.group)
                session.add(new_file)
                session.commit()
                file = new_file

            #Add reading to the file
            file.readings.append(reading)
            reading.TempFile_id = file.id
            if file not in files:
                files.append(file)
        session.commit()

        #For every file that was modified
        for file in files:
            #Update the characteristics of the file
            file_readings = file.readings
            values = []
            for reading in file_readings:
                values.append(reading.value)
            file.min = min(values)
            file.max = max(values)
            file.avg = sum(values) / len(values)
            file.rate = float(len(values)) / 24
        session.commit()


#This function dumps the sensor data from a csv file into the database. Should only be needed once (when the database is created)
def csv_to_sql_temp_data():

    from datetime import datetime, timedelta
    csv = pd.read_csv(temps_path)
    csv.columns=['year', 'month', 'day', 'hour', 'offset', 'temp']

    Session = sessionmaker(bind=engine)

    with Session() as session:
        for row in csv.iterrows():
            date = datetime(year=int(row[1][0]), month=int(row[1][1]), day=int(row[1][2]), hour=int(row[1][3]))
            date = date + timedelta(hours=int(row[1][4]))
            new_reading = TempReading(group='soil', datetime=date, value=row[1][5])
            session.add(new_reading)
        session.commit()

#This function dumps the harvest data from a csv file into the database. Should only be needed once (when the database is created)
def csv_to_sql_harvest_data():

    from datetime import datetime
    csv = pd.read_csv(harvest_path)
    csv.columns=['date', 'name', 'mass']

    Session = sessionmaker(bind=engine)

    with Session() as session:
        for row in csv.iterrows():
            date = datetime.strptime(row[1][0], '%Y-%m-%d')
            plant = session.query(Plant).filter_by(name=row[1][1]).first()
            
            new_entry = HarvestEntry(Plant_id=plant.id, date=date, mass=row[1][2])
            session.add(new_entry)
        session.commit()

#This function will read the plant_attributes csv, find any differences between it and the sql database, and update the sql database
def csv_to_sql():

    csv = pd.read_csv(attributes_path)
    csv.columns=['name', 'active', 'start', 'season', 'min_temp', 'max_temp', 'spring_sow', 'spring_transplant', 'fall_sow', 'cal_g']

    with engine.begin() as connection:
        csv.to_sql('Plant', con=connection, if_exists='replace', index_label='id')


#This function pushes a pandas dataframe into the plants SQL database
def df_to_sql(df):

    logging.info('Printed a plant_attributes dataframe into sql')

    with engine.begin() as connection:
        df.to_sql('Plant', con=connection, if_exists='replace', index_label='id')

#This function will convert the SQL plant database to csv so that it can be manually edited
def sql_to_csv():

    logging.info('Printed a plant_attributes sql into csv')

    with engine.connect() as connection:
        df = pd.read_sql_table('Plant', connection)
        df.iloc[: , 1:].to_csv(attributes_path, index=False)

#This function pulls an sql database into a pandas dataframe and returns it
def get_frame(name):

    with engine.connect() as connection:
        df = pd.read_sql_table(name, connection)
        return df

#This function returns a dataframe with the frost dates
def get_frost_dates():

    df = pd.read_json(frost_path)
    return df

#Dumps the given dict into a json
def frost_to_json(data):

    with open(frost_path, 'w') as file:
        json.dump(data, file)