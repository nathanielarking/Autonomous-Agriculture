from data import engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import and_
import pandas as pd
from data.models import Plant, TempFile
from datetime import date, datetime, timedelta

def generate_calendar(start_date, end_date):

    #Get frost dates
    frost_dates = pd.read_json('data/frost_dates.json')

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

        #Begin construction of temp dataframe with columns and index
        df_temps =  pd.DataFrame(columns=names, index=date_range)
        df_temps.index.name = 'Date'

        #Setting data by looping over every plant and index in data
        for plant in plants:
            
            #Assign sow and transplant values to the planting dataframe
            for date_idx in date_range:

                #Get the frost dates for this year
                first_frost = datetime.strptime(frost_dates['first_frost'][0], '%m/%d').replace(year=date_idx.year)
                last_frost = datetime.strptime(frost_dates['last_frost'][0], '%m/%d').replace(year=date_idx.year)

                #Find planting dates
                spring_sow_date = first_frost + timedelta(days=plant.spring_sow)
                spring_transplant_date = first_frost + timedelta(days=plant.spring_transplant)
                fall_sow_date = last_frost + timedelta(days=plant.fall_sow)


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

            #Assign values to temps table
            for file in temp_files:

                if plant.min_temp < file.min and plant.max_temp > file.max:
                    df_temps[plant.name][file.date] = 0
                else:
                    df_temps[plant.name][file.date] = round(max([plant.min_temp - file.min, file.max - plant.max_temp]), 2)

        #Function to transpose and clean up dataframe
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

        #Apply transform to our tables
        df_list = [df_planting, df_temps]
        df_list = [df.pipe(transform) for df in df_list]

        return df_list

