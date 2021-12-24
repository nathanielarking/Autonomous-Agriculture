from dash import dcc, html, dash_table
from dash_table.Format import Format
import pandas as pd
from webapp.templates.app.colors import palette
import plotly.express as px

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    #Have to predefine the table border as it doesn't allow string formatting
    border_color = palette['border']

    #Import the Plant database, drop the ID and group columns
    from data.interface import get_frame
    df = get_frame('TempFile')
    df = df.drop('id', axis=1)
    df = df.drop('group', axis=1)

    #Grab the minimum and maximum dates found in the dataset for constricting the range picker
    min_date = df['date'].min()
    max_date = df['date'].max()

    fig = px.line(df, x="date", y=df.columns[1:-1])


    layout = html.Div([
        
        dcc.Graph(figure=fig, id='temp-graph'),

        dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=min_date,
        max_date_allowed=max_date,
        start_date=min_date,
        end_date=max_date
        )

        ])

    return layout