from dash import dcc, html, dash_table
import pandas as pd
from webapp.templates.app.colors import palette, picker_style, dropdown_style
from sqlalchemy.orm import sessionmaker
from data import engine
from data.models import Plant
from data.interface import update_temp_file
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

#Define our custom template for this plotly graph
pio.templates['custom_template'] = go.layout.Template(
    layout_paper_bgcolor=palette['col4'],
    layout_plot_bgcolor=palette['col3']
)
pio.templates.default = 'plotly_dark+custom_template'

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    #Have to predefine the table border as it doesn't allow string formatting
    border_color = palette['border']

    #Update the temp file table from the temp reading table
    update_temp_file()

    #Import the Plant database, drop the ID and group columns
    from data.interface import get_frame
    df = get_frame('TempFile')
    df = df.drop('id', axis=1)
    df = df.drop('group', axis=1)

    #Grab the minimum and maximum dates found in the dataset for constricting the range picker
    #min_date = df['date'].min()
    min_date = datetime(datetime.today().year, 1, 1)
    max_date = df['date'].max()

    fig = px.line(df, x="date", y=df.columns[1:-1])

    fig.update_yaxes(
    ticktext=[i for i in range(0, 45, 5)],
    tickvals=[i for i in range(0, 45, 5)],
    )

    Session = sessionmaker(bind=engine)

    options = []
    with Session() as session:
        options = [
        {"label": plant.name, "value": plant.name}
        for plant in session.query(Plant).all()
        ]


    layout = html.Div([
        
        dcc.Graph(figure=fig, id='temp-graph'),

        html.Div([

            dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date,
            style=picker_style
            ),

            dcc.Dropdown(
                id='plant-picker',
                options=options,
                value=None,
                multi=False,
                placeholder='Select Plants',
                style=dropdown_style
            ),


        ])

        ])

    return layout