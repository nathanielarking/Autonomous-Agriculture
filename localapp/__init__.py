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

#connect database object to database
engine = create_engine(f'sqlite:///data/{DB_NAME}', echo=True)

def create_localapp():

    #Create it if it does not already exist
    from data.models import User, Plant
    if not path.exists('data/' + DB_NAME):
        Base.metadata.create_all(bind=engine)
        logging.info('Created Webapp Database')

    #Session = sessionmaker(bind=engine)
    #session = Session()

    