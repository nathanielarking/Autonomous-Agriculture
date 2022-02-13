from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

#Import object which contains the dashboard objects
from webapp.dashapps import container as dashboards
#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

#Script to grab frost dates from database
from data.interface import get_frost_dates

settings_blueprint = Blueprint('settings_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Page to view and edit the csv containing attributes for plants
@settings_blueprint.route('/settings/attributes')
@login_required
def attributes():

    dash_html = dashboards.get('attributes').index()
    return render_template('settings/attributes.html', user=current_user, dash_html=dash_html, palette=palette)

#Page to view and edit the csv containing attributes for plants
@settings_blueprint.route('/settings/frost_dates')
@login_required
def frost_dates():

    dash_html = dashboards.get('frost_dates').index()
    return render_template('settings/frost_dates.html', user=current_user, palette=palette, dash_html=dash_html)