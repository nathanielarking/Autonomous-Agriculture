from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

#Import object which contains the dashboard objects
from webapp.dashapps import container as dashboards
#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

sensors_blueprint = Blueprint('sensors_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Route to view the sensor data
@sensors_blueprint.route('/sensors/')
@login_required
def sensors():
    return render_template('sensors/sensors.html', user=current_user, palette=palette)