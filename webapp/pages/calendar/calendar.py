from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

#Import object which contains the dashboard objects
from webapp.dashapps import container as dashboards
#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

calendar_blueprint = Blueprint('calendar_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Route to view the generated planting calendar
@calendar_blueprint.route('/calendar/chart')
@login_required
def chart():
    dash_html = dashboards.get('calendar_chart').index()
    return render_template('calendar/chart.html', user=current_user, palette=palette, dash_html=dash_html)