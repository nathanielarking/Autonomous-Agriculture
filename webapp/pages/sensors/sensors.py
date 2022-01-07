from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

#Import object which contains the dashboard objects
from webapp.dashapps import container as dashboards
#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

sensors_blueprint = Blueprint('sensors_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Route to view the sensor graphs
@sensors_blueprint.route('/sensors/graphs')
@login_required
def graphs():
    dash_html = dashboards.get('sensor_graphs').index()
    return render_template('sensors/graphs.html', user=current_user, dash_html=dash_html, palette=palette)

#Route to view the sensor data
@sensors_blueprint.route('/sensors/data')
@login_required
def data():
    dash_html = dashboards.get('sensor_data').index()
    return render_template('sensors/data.html', user=current_user, dash_html=dash_html, palette=palette)