from . import db
from flask_login import UserMixin

#Class to store user login data in a database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    admin = db.Column(db.Boolean)

#Class to store plant data in a database
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    active = db.Column(db.Boolean)
    start = db.Column(db.String(10))
    season = db.Column(db.String(5))
    min_temp = db.Column(db.Integer)
    max_temp = db.Column(db.Integer)
    spring_sow = db.Column(db.Integer)
    spring_transplant = db.Column(db.Integer)
    fall_sow = db.Column(db.Integer)
    calories = db.Column(db.Float)


#Class to store sensor data in a database

#Class to store harvest data in a database