from dash import dcc, html, dash_table
from dash.dash_table.Format import Format
import pandas as pd
from webapp.templates.app.colors import palette
from datetime import datetime
from data import engine
from sqlalchemy.orm import Session
from data.models import Plant

#Have to predefine the table border as it doesn't allow string formatting
border_color = palette['border']

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    #Import the harvest entry database, drop the ID and group columns
    from data.interface import get_frame
    df = get_frame('HarvestEntry')

    #Get the names of plants and the calorie values
    names = []
    cals = []
    with Session(engine) as session:
        for id in df['Plant_id']:
            plant = session.query(Plant).filter_by(id=id).first()
            names.append(plant.name)
            cals.append(plant.cal_g)
    df['Plant'] = names
    df['Calories'] = df['mass'].multiply(cals, axis='index')

    #Drop unneccesary columns
    df = df.drop('id', axis=1)
    df = df.drop('Plant_id', axis=1)
    #Format columns
    df['date'] = df['date'].dt.date
    #df['Calories'] = df['Calories'].map('{:,.2f}'.format)
    df = df[['Plant', 'date', 'mass', 'Calories']]
    df = df.rename(columns={'date': 'Date', 'mass': 'Mass (g)'})

    layout = html.Div([

        dash_table.DataTable(
            id='sensor_data-table',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False, 'type': 'numeric', "format": Format(precision=4)}
                for i in df.columns
            ],
            data=df.to_dict('records'),
            filter_action="native", #Allows filtering 
            sort_action="native", #Allows sorting
            sort_mode="single", #Sorts a single column at a time or multi columns
            column_selectable="none", #Allows/disallows the selecting of rows/columns
            page_action="native",
            page_current=0, #Default start is on first page
            page_size=45,
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': palette['col2'],
                }
            ],
            style_data={ #Overflow cell contents onto next line
                'whiteSpace': 'normal',
                'height': 'auto',
                'overflowX': 'auto',
                'color': palette['text_body'],
                'backgroundColor': palette['col1']
            },
            style_filter={
                'backgroundColor': palette['col0'],
                'color': palette['text_body'],
            },
            style_header={
                'backgroundColor': palette['col0'],
                'color': palette['text_title'],
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['name', 'active', 'start', 'season']
            ],
            style_cell={
                'minWidth': 95, 'maxWidth': 95, 'width': 95,
                'font-family': 'monospace',
                'color': palette['text_body'],
                'backgroundColor': palette['background'],
                'border':  f'3px solid {border_color}'
            }
            ),

        ])

    return layout

