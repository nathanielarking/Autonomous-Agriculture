from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

#Import object which contains the dashboard objects
from webapp.dashapps import container as dashboards
#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

home_blueprint = Blueprint('home_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Home route 
@home_blueprint.route('/')
@login_required
def home():
    return render_template('home/home.html', user=current_user, palette=palette)