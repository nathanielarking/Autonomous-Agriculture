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

#Route to add new planting entries graphs
@entry_blueprint.route('/entry/planting', methods=['GET', 'POST'])
@login_required
def entry_planting():

    #Get the names of plants
    names = []
    with Session(engine) as session:
        plants = session.query(Plant).filter_by(active=1).all()
        for plant in plants:
            names.append(plant.name)

    current_day = date.today().strftime("%Y-%m-%d")

    #Add new planting to the database
    if request.method == "POST":
        #Assign variables from request
        name = request.form.get('name')
        entry_date = request.form.get('date')
        entry_date = datetime.strptime(entry_date, "%Y-%m-%d")
        description = request.form.get('description')

        if description is not None:
            with Session(engine) as session:
                plant = session.query(Plant).filter_by(name=name).one()
                entry = PlantingEntry(Plant_id=plant.id, Plant=plant, date=entry_date, description=description)
                session.add(entry)
                session.commit()

    return render_template('entry/planting.html', user=current_user, palette=palette, names=names, current_day=current_day)

#Route to add new harvest entries
@entry_blueprint.route('/entry/harvest', methods=['GET', 'POST'])
@login_required
def entry_harvest():

    #Get the names of plants
    names = []
    with Session(engine) as session:
        plants = session.query(Plant).filter_by(active=1).all()   
        for plant in plants:
            names.append(plant.name)

    current_day = date.today().strftime("%Y-%m-%d")

    #Add new planting to the database
    if request.method == "POST":
        #Assign variables from request
        name = request.form.get('name')
        entry_date = request.form.get('date')
        entry_date = datetime.strptime(entry_date, "%Y-%m-%d")
        mass = request.form.get('mass')

        if mass is not None:
            with Session(engine) as session:
                plant = session.query(Plant).filter_by(name=name).one()
                print(plant.id)
                print(plant)
                print(entry_date)
                print(mass)
                entry = HarvestEntry(Plant_id=plant.id, Plant=plant, date=entry_date, mass=mass)
                session.add(entry)
                session.commit()

    return render_template('entry/harvest.html', user=current_user, palette=palette, names=names, current_day=current_day)