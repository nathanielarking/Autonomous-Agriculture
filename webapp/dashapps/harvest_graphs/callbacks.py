from dash.dependencies import Input, Output
from .layout import total_layout, annual_layout
from sqlalchemy.orm import Session
from data import engine
from data.models import Plant, HarvestEntry
import pandas as pd
import datetime
import plotly.express as px

def register_callbacks(dashapp):

    #Register change between tabs
    @dashapp.callback(
        Output('block-content', 'children'),
        Input('harvest-tabs', 'value')
    )
    def render_tabs(tab):
        if tab =='total-tab':
            return total_layout

        elif tab == 'annual-tab':
            return annual_layout

    #Register changes for total graphs config
    @dashapp.callback(
        Output('total_bar_date', 'figure'),
        Output('total_bar_plant', 'figure'),
        Output('total_pie', 'figure'),
        Input('total_mode-picker', 'value')
    )
    def update_total(mode):
        name = []
        date = []
        mass = []
        cals = []
        years = []
        #Loop through all harvest entries which contain year 
        with Session(engine) as session:
            entries = session.query(HarvestEntry)
            for entry in entries:
                plant = session.query(Plant).filter_by(id=entry.Plant_id).first()
                name.append(plant.name)
                mass.append(entry.mass / 1000)
                cals.append(entry.mass * plant.cal_g)
                years.append(entry.date.year)

        data = {'Plant': name, 'Year': years, 'Mass': mass, 'Calories': cals}
        df = pd.DataFrame(data)

        if mode == 'mass':

            fig_bar_date = px.histogram(df, x='Year', y='Mass', color = 'Plant', barmode='group', title='Mass of Harvests by Year')
            fig_bar_plant = px.histogram(df, x='Plant', y='Mass', title='Mass of Harvests by Plant')
            fig_pie = px.pie(df, values = 'Mass', names='Plant', title=f'Total: {round(sum(mass), 2)} kg')

        elif mode == 'cals':
            
            fig_bar_date = px.histogram(df, x='Year', y='Calories', color = 'Plant', barmode='group', title='Calories of Harvests by Year')
            fig_bar_plant = px.histogram(df, x='Plant', y='Calories', title='Calories of Harvests by Plant')
            fig_pie = px.pie(df, values = 'Calories', names='Plant', title=f'Total: {round(sum(cals), 2)} calories')

        return fig_bar_date, fig_bar_plant, fig_pie

    #Register changes for annual graphs config
    @dashapp.callback(
        Output('annual_bar_date', 'figure'),
        Output('annual_bar_plant', 'figure'),
        Output('annual_pie', 'figure'),
        Input('year-picker', 'value'),
        Input('annual_mode-picker', 'value')
    )
    def update_annual(year, mode):
        name = []
        date = []
        mass = []
        cals = []
        start_date = datetime.datetime(int(year), 1, 1)
        end_date = datetime.datetime(int(year)+1, 1, 1)
        #Loop through all harvest entries which contain year 
        with Session(engine) as session:
            entries = session.query(HarvestEntry).filter(HarvestEntry.date >= start_date, HarvestEntry.date < end_date).all()
            for entry in entries:
                plant = session.query(Plant).filter_by(id=entry.Plant_id).first()
                name.append(plant.name)
                date.append(entry.date)
                mass.append(entry.mass / 1000)
                cals.append(entry.mass * plant.cal_g)

        data = {'Plant': name, 'Date': date, 'Mass': mass, 'Calories': cals}
        df = pd.DataFrame(data)

        if mode == 'mass':

            fig_bar_date = px.bar(df, x='Date', y='Mass', color = 'Plant', title='Mass of Harvests by Date')
            fig_bar_plant = px.bar(df, x='Plant', y='Mass', title='Mass of Harvests by Plant')
            fig_pie = px.pie(df, values = 'Mass', names='Plant', title=f'Total: {round(sum(mass), 2)} kg')

        elif mode == 'cals':
            
            fig_bar_date = px.bar(df, x='Date', y='Calories', color = 'Plant', title='Calories of Harvests by Date')
            fig_bar_plant = px.bar(df, x='Plant', y='Calories', title='Calories of Harvests by Plant')
            fig_pie = px.pie(df, values = 'Calories', names='Plant', title=f'Total: {round(sum(cals), 2)} calories')

        return fig_bar_date, fig_bar_plant, fig_pie
    

