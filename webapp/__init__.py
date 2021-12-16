from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
import dash
import logging

#Import environment variables
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
DB_NAME = str(os.getenv('DATABASE_NAME'))
SECRET_KEY = str(os.getenv('SECRET_KEY'))

#Create SQL database object
db = SQLAlchemy()

#Initialize and return flask application
def create_webapp():
    #Create instance of flask object
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Set secret key of the application
    flask_app.config['SECRET_KEY'] = SECRET_KEY
    #Link flask and create SQL database
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///../data/{DB_NAME}'
    db.init_app(flask_app)

    #Import and assign objects from blueprint files
    from .views import views
    from .auth import auth
    flask_app.register_blueprint(views, urlprefix='/')
    flask_app.register_blueprint(auth, urlprefix='/')

    #Create login manager to handle user logins
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(flask_app)
    
    #Define how login manager can load users
    from data.models import User
    @login_manager.user_loader
    def load_user(id):
        return db.session.query(User).get(int(id))

    #Register dashboards
    from .dashapps import create_dashboards
    create_dashboards(flask_app)

    return flask_app
