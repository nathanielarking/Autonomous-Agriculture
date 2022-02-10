from flask import Blueprint, render_template, request, flash
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
photos_path = os.path.dirname(photos_path)
photos_path = os.path.join(photos_path, 'localapp/photos')

#Home route 
@home_blueprint.route('/')
@login_required
def home():

    #list_of_pics = glob.glob(f'{photos_path}/*') # * means all if need specific format then *.csv
    #latest_pic = max(list_of_files, key=os.path.getctime)

    return render_template('home/home.html', user=current_user, palette=palette)