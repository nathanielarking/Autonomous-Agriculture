from . import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

#Note: when adding new models, update the initialization of the tables in init.py

#Class to store userdata for webapp
class User(Base, UserMixin):

    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    password = Column(String(150), nullable=False)
    username = Column(String(150), nullable=False)
    admin = Column(Boolean, default=False)

#Class to store plant data in a database
class Plant(Base):

    __tablename__ = "Plant"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable = False)
    active = Column(Boolean, nullable=False)
    start = Column(String(10), nullable=False)
    season = Column(String(5), nullable=False)
    min_temp = Column(Integer, nullable=False)
    max_temp = Column(Integer, nullable=False)
    spring_sow = Column(Integer, nullable=False)
    spring_transplant = Column(Integer, nullable=False)
    fall_sow = Column(Integer, nullable=False)
    cal_g = Column(Float, nullable=False)

    harvests = relationship("HarvestEntry", back_populates="Plant")
    plantings = relationship("PlantingEntry", back_populates="Plant")

#Class to store sensor data in a database
class TempReading(Base):

    __tablename__ = "TempReading"

    id = Column(Integer, primary_key=True)
    group = Column(String(15))
    datetime = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)

    TempFile_id = Column(Integer, ForeignKey('TempFile.id'))
    TempFile = relationship("TempFile", back_populates="readings")

#Class to file temperature values and find the average, minimum, and maximum
class TempFile(Base):

    __tablename__ = "TempFile"

    id = Column(Integer, primary_key=True)
    group = Column(String(15))
    date = Column(Date, nullable=False, unique=True)
    readings = relationship("TempReading", back_populates="TempFile")

    min = Column(Float)
    max = Column(Float)
    avg = Column(Float)
    rate = Column(Float)

#Class to store sensor data in a database
class MoistReading(Base):

    __tablename__ = "MoistReading"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    value = Column(Integer, nullable=False)

#Class to store harvest data in a database
class HarvestEntry(Base):

    __tablename__ = "HarvestEntry"
    id = Column(Integer, primary_key=True)
    Plant_id = Column(Integer, ForeignKey('Plant.id'))
    Plant = relationship("Plant", back_populates="harvests")
    mass = Column(Float)
    date = Column(Date)

#Class to store planting descriptions in the database
class PlantingEntry(Base):

    __tablename__ = "PlantingEntry"
    id = Column(Integer, primary_key=True)
    Plant_id = Column(Integer, ForeignKey('Plant.id'))
    Plant = relationship("Plant", back_populates="plantings")
    date = Column(Date)
    description = Column(String)