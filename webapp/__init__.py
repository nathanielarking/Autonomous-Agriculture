from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import logging

#Create SQL database
db = SQLAlchemy()
DB_NAME = "database.db"

#Initialize and return flask application
def create_app():
    #Create instance of flask object
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Set secret key of the application
    app.config['SECRET_KEY'] = 'n14h29bnnf378n309'
    #Link flask and create SQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #Import and assign objects from blueprint files
    from .views import views
    from .auth import auth
    app.register_blueprint(views, urlprefix='/')
    app.register_blueprint(auth, urlprefix='/')

    #Import and create database
    from .models import User
    create_database(app)

    #Create login manager to handle user logins
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
      
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#Create a database if it does not already exist
def create_database(app):
    if not path.exists('webapp/' + DB_NAME):
        db.create_all(app=app)
        logging.info('Created Webapp Database')
