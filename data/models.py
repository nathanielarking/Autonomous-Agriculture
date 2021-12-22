from localapp import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from flask_login import UserMixin

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
    name = Column(String(100), unique=True)
    active = Column(Boolean)
    start = Column(String(10))
    season = Column(String(5))
    min_temp = Column(Integer)
    max_temp = Column(Integer)
    spring_sow = Column(Integer)
    spring_transplant = Column(Integer)
    fall_sow = Column(Integer)
    cal_g = Column(Float)

    @classmethod
    def get_first(cls, session, name):
        return session.query(cls).filter_by(name=name).first()

#Class to store sensor data in a database

#Class to store harvest data in a database