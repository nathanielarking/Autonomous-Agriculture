import pandas as pd
from sqlalchemy.orm import Session
from .models import Plant
import logging

from localapp import engine

#This function will read the plant_attributes csv, find any differences between it and the sql database, and update the sql database
def csv_to_sql():

    csv = pd.read_csv('data/plant_attributes.csv')
    logging.info('Printed a plant_attributes csv into sql')

    with engine.begin() as connection:
        csv.to_sql('Plant', con=connection, if_exists='replace', index_label='Index')

#This function pushes a pandas dataframe into the plants SQL database
def df_to_sql(df):

    logging.info('Printed a plant_attributes dataframe into sql')

    with engine.begin() as connection:
        df.to_sql('Plant', con=connection, if_exists='replace', index_label='Index')

#This function will convert the SQL plant database to csv so that it can be manually edited
def sql_to_csv():

    logging.info('Printed a plant_attributes sql into csv')

    with engine.connect() as connection:
        df = pd.read_sql_table('Plant', connection)
        df.iloc[: , 1:].to_csv('data/plant_attributes.csv', index=False)

#This function pulls an sql database into a pandas dataframe and returns it
def get_frame(name):

    with engine.connect() as connection:
        df = pd.read_sql_table(name, connection)
        return df