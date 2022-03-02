from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required, current_user

#Import object which contains the dashboard objects
from webapp.dashapps import container as dashboards
#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

import glob
import os

home_blueprint = Blueprint('home_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Import photos path
photos_path = os.path.dirname(__file__)
photos_path = os.path.dirname(photos_path)
photos_path = os.path.dirname(photos_path)
photos_path = os.path.join(photos_path, 'static', 'photos')

#Home route 
@home_blueprint.route('/')
@login_required
def home():

    #Grab list of photos in static photos path
    list_of_photos = glob.glob(f'{photos_path}/*.png') # * means all if need specific format then *.csv
    #Find latest photos
    latest_photo = max(list_of_photos, key=os.path.getctime)
    #Remove directory from file path
    latest_photo = os.path.basename(latest_photo)
    #Add onto photos subfolder
    photo_path = os.path.join('photos', latest_photo)
    #Connect photo path to static directory
    photo_url = url_for('static', filename=photo_path)

    return render_template('home/home.html', user=current_user, palette=palette, photo_url=photo_url)