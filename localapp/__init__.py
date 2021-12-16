from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import path
import logging

#Import environment variables
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
DB_NAME = str(os.getenv('DATABASE_NAME'))

#Create object for interacting with SQL database
Base = declarative_base()

def create_localapp():

    #connect database object to database
    engine = create_engine(f'sqlite:///data/{DB_NAME}', echo=True)
    #Create it if it does not already exist
    from data.models import User, Plant
    if not path.exists('data/' + DB_NAME):
        Base.metadata.create_all(bind=engine)
        logging.info('Created Webapp Database')

    from data.interface import csv_to_sql
    Session = sessionmaker(bind=engine)
    session = Session()
    
    from data.interface import sql_to_csv
    conne = engine.connect()
    sql_to_csv(conne)

    