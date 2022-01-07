from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

#Import object which contains the dashboard objects
from webapp.dashapps import container as dashboards
#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

harvest_blueprint = Blueprint('harvest_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Route to view the harvest graphs
@harvest_blueprint.route('/harvest/graphs')
@login_required
def graphs():
    dash_html = dashboards.get('harvest_graphs').index()
    return render_template('harvest/graphs.html', user=current_user, dash_html=dash_html, palette=palette)

#Route to view the harvest data
@harvest_blueprint.route('/harvest/data')
@login_required
def data():
    dash_html = dashboards.get('harvest_data').index()
    return render_template('harvest/data.html', user=current_user, dash_html=dash_html, palette=palette)