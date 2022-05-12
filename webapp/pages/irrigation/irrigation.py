from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from data import engine
from sqlalchemy.orm import Session
#from data.models import Plant, HarvestEntry, PlantingEntry
from datetime import date, datetime

#Import object which contains the dashboard objects
from webapp.dashapps import container as dashboards
#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

irrigation_blueprint = Blueprint('irrigation_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Route to control the manual schedule and eventually AI scheduling
@irrigation_blueprint.route('/irrigation/schedule', methods=['GET', 'POST'])
@login_required
def irrigation_schedule():

        return render_template('irrigation/schedule.html', user=current_user, palette=palette)

#Route to manually control the irrigation
@irrigation_blueprint.route('/irrigation/control', methods=['GET', 'POST'])
@login_required
def irrigation_control():
    dash_html = dashboards.get('irrigation_control').index()
    return render_template('irrigation/control.html', user=current_user, dash_html=dash_html, palette=palette)

#Route to view the history and data of past irrigation actions
@irrigation_blueprint.route('/irrigation/history', methods=['GET', 'POST'])
@login_required
def irrigation_history():

    return render_template('irrigation/history.html', user=current_user, palette=palette)