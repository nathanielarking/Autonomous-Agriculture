from flask import Blueprint, render_template
from flask_login import login_required, current_user 

#Create blueprint object to hold URLs
views = Blueprint('views', __name__)

#Home route 
@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

#Route to view the generated planting calendar
@views.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', user=current_user)

#Route to view the sensor data
@views.route('/sensors')
@login_required
def sensors():
    return render_template('sensors.html', user=current_user)

#Route to view and edit harvest data
@views.route('/harvest')
@login_required
def harvest():
    return render_template('harvest.html', user=current_user)

#Page to view and edit the csv containing attributes for plants
@views.route('/attributes')
@login_required
def attributes():
    return render_template('attributes.html', user=current_user)



