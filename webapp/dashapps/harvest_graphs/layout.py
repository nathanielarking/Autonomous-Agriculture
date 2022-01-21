from dash import dcc, html, dash_table
import pandas as pd
from webapp.templates.app.colors import palette, tab_style, tabs_style, tab_selected_style, dropdown_style
import plotly.express as px
from sqlalchemy.orm import Session
from data import engine
from data.models import HarvestEntry, Plant

years = []
#Loop through all harvest entries which contain year 
with Session(engine) as session:
    entries = session.query(HarvestEntry).all()
    for entry in entries:
        if entry.date.year not in years:
            years.append(entry.date.year)
options = [
        {"label": year, "value": year}
        for year in years
        ]

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    layout = html.Div([

    dcc.Tabs(id='harvest-tabs', value='annual-tab', style=tabs_style, children=[
            dcc.Tab(label='Total', value='total-tab', style=tab_style, selected_style = tab_selected_style),
            dcc.Tab(label='Annual', value='annual-tab', style=tab_style, selected_style = tab_selected_style)
        ]),
        html.Div(id='block-content')

])
    return layout

def serve_total_layout():

    total_layout = html.Div([

        dcc.RadioItems(
            id='total_mode-picker',
            options=[
                {'label': 'Display Mass', 'value': 'mass'},
                {'label': 'Display Calories', 'value': 'cals'}
            ],
            value='mass'
        ),

        dcc.Graph(id='total_bar_date', figure=px.bar()),
        dcc.Graph(id='total_bar_plant', figure=px.bar()),
        dcc.Graph(id='total_pie', figure=px.bar())

    ])

    return total_layout

def serve_annual_layout():

    annual_layout = html.Div([
        
        dcc.Dropdown(
                    id='year-picker',
                    options=options,
                    value=options[-1]['value'],
                    multi=False,
                    placeholder='Select Year',
                    style=dropdown_style
                ),

        dcc.RadioItems(
            id='annual_mode-picker',
            options=[
                {'label': 'Display Mass', 'value': 'mass'},
                {'label': 'Display Calories', 'value': 'cals'}
            ],
            value='mass'
        ),

        dcc.Graph(id='annual_bar_date', figure=px.bar()),
        dcc.Graph(id='annual_bar_plant', figure=px.bar()),
        dcc.Graph(id='annual_pie', figure=px.bar())

    ])

    return annual_layout