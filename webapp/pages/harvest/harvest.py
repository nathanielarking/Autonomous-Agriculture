from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

#Import object which contains the dashboard objects
from webapp.dashapps import container as dashboards
#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

harvest_blueprint = Blueprint('harvest_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Route to view and edit harvest data
@harvest_blueprint.route('/harvest/')
@login_required
def harvest():  
    return dashboards.get('harvest').index()
    #return render_template('harvest.html', user=current_user)