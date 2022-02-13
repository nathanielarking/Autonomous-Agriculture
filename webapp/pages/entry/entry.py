from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from data import engine
from sqlalchemy.orm import Session
from data.models import Plant, HarvestEntry, PlantingEntry
from datetime import date, datetime

#Import colors to insert into the CSS
from webapp.templates.app.colors import palette

entry_blueprint = Blueprint('entry_blueprint', __name__,
    template_folder='templates',
    static_folder='static')

#Route to view the harvest graphs
@entry_blueprint.route('/entry/planting', methods=['GET', 'POST'])
@login_required
def entry_planting():

    #Get the names and variety of plants
    names = []
    variety = 0
    with Session(engine) as session:
        plants = session.query(Plant).filter_by(active=1).all()
            
        for plant in plants:
            names.append(plant.name)
            variety += 1

    current_day = date.today().strftime("%Y-%m-%d")

    #Add new planting to the database
    if request.method == "POST":
        #Assign variables from request
        name = request.form.get('name')
        entry_date = request.form.get('date')
        entry_date = datetime.strptime(entry_date, "%Y-%m-%d")
        description = request.form.get('description')

        with Session(engine) as session:
            plant = session.query(Plant).filter_by(name=name).one()
            entry = PlantingEntry( Plant_id=plant.id, Plant=plant, date=entry_date, description=description)
            session.add(entry)
            session.commit()

    return render_template('entry/planting.html', user=current_user, palette=palette, names=names, current_day=current_day)

#Route to view the harvest data
@entry_blueprint.route('/entry/harvest')
@login_required
def entry_harvest():

    return render_template('entry/harvest.html', user=current_user, palette=palette)