from data import engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import and_
import pandas as pd
from data.interface import get_frost_dates
from data.models import Plant, TempFile, PlantingEntry
from datetime import date, datetime, timedelta

#Clean up and transpose calendar dataframes
def transform(df):
    df = df.reset_index()
    df['Date'] = df['Date'].dt.strftime("%b %d")

    #Transpose frames and fix columns and headers
    df = df.T
    df.columns = df.iloc[0]
    df = df[1:]

    #Fix index name
    df.index.name = 'Name'
    df = df.reset_index()

    return df

def generate_planting_calendar(start_days, end_days):

    #Get frost dates
    frost_dates = get_frost_dates()

    #Get start and end days for the calendar
    current_date = date.today()
    start_date = current_date - timedelta(days=start_days)
    end_date = current_date + timedelta(days=end_days)

    with Session(engine) as session:

        #Grab list of plants and names of plants in a list
        plants = session.query(Plant).filter_by(active=True).all()
        names = []
        for plant in plants:
            names.append(plant.name)

        #Get range of dates
        date_range = pd.date_range(start_date, end_date)
        #Grabbing tempfiles in our date range
        temp_files = session.query(TempFile).filter(and_(TempFile.date>=start_date, TempFile.date<=end_date))

        #Begin construction of planting dataframe with columns and index
        df_planting = pd.DataFrame(columns=names, index=date_range)
        df_planting.index.name = 'Date'

        #Setting data by looping over every plant and index in data
        for plant in plants:
            
            #Assign sow and transplant values to the planting dataframe
            for date_idx in date_range:

                #Get the frost dates for this year
                last_frost = datetime.strptime(frost_dates['last_frost'][0], '%m/%d').replace(year=date_idx.year)
                first_frost = datetime.strptime(frost_dates['first_frost'][0], '%m/%d').replace(year=date_idx.year)

                #Find planting dates
                spring_sow_date = last_frost + timedelta(days=plant.spring_sow)
                spring_transplant_date = last_frost + timedelta(days=plant.spring_transplant)
                fall_sow_date = first_frost + timedelta(days=plant.fall_sow)


                #Assign values
                if plant.season == 'warm':

                    if plant.start == 'indoors':
                        if date_idx == spring_sow_date: df_planting[plant.name][date_idx] = 'Sow'
                        if date_idx == spring_transplant_date: df_planting[plant.name][date_idx] = 'Transplant'

                    elif plant.start == 'direct':
                        if date_idx == spring_sow_date: df_planting[plant.name][date_idx] = 'Sow'

                elif plant.season == 'cool':

                    if plant.start == 'indoors':
                        if date_idx == spring_sow_date: df_planting[plant.name][date_idx] = 'Sow'
                        if date_idx == spring_transplant_date: df_planting[plant.name][date_idx] = 'Transplant'

                    elif plant.start == 'direct':
                        if date_idx == spring_sow_date: df_planting[plant.name][date_idx] = 'Sow'

                    if date_idx == fall_sow_date: df_planting[plant.name][date_idx] = 'Sow'

        return transform(df_planting)

def generate_temps_calendar(start_days, end_days):

    #Get frost dates
    frost_dates = get_frost_dates()

    #Get start and end days for the calendar
    current_date = date.today()
    start_date = current_date - timedelta(days=start_days)
    end_date = current_date + timedelta(days=end_days)

    with Session(engine) as session:

        #Grab list of plants and names of plants in a list
        plants = session.query(Plant).filter_by(active=True).all()
        names = []
        for plant in plants:
            names.append(plant.name)

        #Get range of dates
        date_range = pd.date_range(start_date, end_date)
        #Grabbing tempfiles in our date range
        temp_files = session.query(TempFile).filter(and_(TempFile.date>=start_date, TempFile.date<=end_date))

        #Begin construction of temp dataframe with columns and index
        df_temps =  pd.DataFrame(columns=names, index=date_range)
        df_temps.index.name = 'Date'

        #Setting data by looping over every plant and index in data
        for plant in plants:

            #Assign values to temps table
            for file in temp_files:

                if plant.min_temp < file.min and plant.max_temp > file.max:
                    df_temps[plant.name][file.date] = 0
                else:
                    df_temps[plant.name][file.date] = round(max([plant.min_temp - file.min, file.max - plant.max_temp]), 2)

        return transform(df_temps)

def generate_record_calendar(start_days, end_days):

    #Get start and end days for the calendar
    current_date = date.today()
    start_date = current_date - timedelta(days=start_days)
    end_date = current_date + timedelta(days=end_days)

    with Session(engine) as session:

        #Grab list of plants and names of plants in a list
        plants = session.query(Plant).filter_by(active=True).all()
        names = []
        for plant in plants:
            names.append(plant.name)

        #Get range of dates
        date_range = pd.date_range(start_date, end_date)

        #Begin construction of record dataframe with columns and index
        df_record =  pd.DataFrame(columns=names, index=date_range)
        df_record.index.name = 'Date'

        #Setting data by looping over every plant and index in data
        for plant in plants:

            #Grabbing records in our date range for this plant
            records = session.query(PlantingEntry).filter_by(Plant_id=plant.id).filter(and_(PlantingEntry.date>=start_date, PlantingEntry.date<=end_date)).all()

            #Assign values to records table
            for planting in records:
                df_record[plant.name][planting.date] = planting.description

        return transform(df_record)

def get_date_columns():
    
    #Get the values for important days that will be in the columns of the table
    frost_dates = get_frost_dates()
    last_frost_date = datetime.strptime(frost_dates['last_frost'][0], '%m/%d')
    first_frost_date = datetime.strptime(frost_dates['first_frost'][0], '%m/%d')
    current_date = date.today()

    last_frost_column = last_frost_date.strftime("%b %d")
    first_frost_column = first_frost_date.strftime("%b %d")
    current_column = current_date.strftime("%b %d")

    return last_frost_column, first_frost_column, current_column