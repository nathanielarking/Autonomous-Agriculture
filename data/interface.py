import pandas as pd
from sqlalchemy.orm import sessionmaker
from .models import Plant

#This function will read the plant_attributes csv, find any differences between it and the sql database, and update the sql database
def csv_to_sql(session):

    csv = pd.read_csv('data/plant_attributes.csv')
    
    for row in csv.itertuples():

        #Grab plant from database with same name, if it exists then update it, otherwise add it
        plant = Plant.get_first(session, row[1])
        if plant:
            if plant.active != row[2]:            plant.active = row[2]
            if plant.start != row[3]:             plant.start = row[3]
            if plant.season != row[4]:            plant.season = row[4]
            if plant.min_temp != row[5]:          plant.min_temp = row[5]
            if plant.max_temp != row[6]:          plant.max_temp = row[6]
            if plant.spring_sow != row[7]:        plant.spring_sow = row[7]
            if plant.spring_transplant != row[8]: plant.spring_transplant = row[8]
            if plant.fall_sow != row[9]:          plant.fall_sow = row[9]
            if plant.cal_g != row[10]:            plant.cal_g = row[10]
        else:
            new_plant = Plant(name=row[1], active=row[2], start=row[3], season=row[4], min_temp=row[5], max_temp=row[6], spring_sow=row[7], spring_transplant=row[8], fall_sow=row[9], cal_g=row[10])
            session.add(new_plant)

    #Commit changes to the database
    session.commit()

#This function will convert the SQL plant database to csv so that it can be manually edited
def sql_to_csv(connection):

    df = pd.read_sql_table('Plant', connection)
    df.iloc[: , 1:].to_csv('data/plant_attributes.csv', index=False)