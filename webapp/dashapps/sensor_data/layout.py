from dash import dcc, html, dash_table
from dash_table.Format import Format
import pandas as pd
from webapp.templates.app.colors import palette
from datetime import datetime

#Have to predefine the table border as it doesn't allow string formatting
border_color = palette['border']


#Import the tempfile database, drop the ID and group columns
from data.interface import get_frame
df_summary = get_frame('TempFile')
df_summary = df_summary.drop('id', axis=1)
df_summary = df_summary.drop('group', axis=1)
#Format columns
df_summary['date'] = df_summary['date'].dt.date
df_summary['min'] = df_summary['min'].map('{:,.2f}°'.format)
df_summary['max'] = df_summary['max'].map('{:,.2f}°'.format)
df_summary['avg'] = df_summary['avg'].map('{:,.2f}°'.format)
df_summary.loc[:,'rate'] *= 100
df_summary['rate'] = df_summary['rate'].map('{:,.2f}%'.format)
df_summary.rename(columns={'date': 'Date', 'min': 'Minimim Temperature (C)', 'max': 'Maximum Temperature (C)', 'avg': 'Average Temperature (C)', 'rate': 'Data Success Rate'}, inplace=True)

#Import the temp reading database, drop the ID column, group column, and column containing relationship to temp file
df_raw = get_frame('TempReading')
df_raw = df_raw.drop('id', axis=1)
df_raw = df_raw.drop('group', axis=1)
df_raw = df_raw.drop('TempFile_id', axis=1)
#Format columns
df_raw['value'] = df_raw['value'].map('{:,.2f}°'.format)
df_raw.rename(columns={'datetime': 'Date and time', 'value': 'Temperature (C)'}, inplace=True)

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    layout = html.Div([

        dcc.Tabs(id='data-tabs', value='summary-tab', children=[
            dcc.Tab(label='summary-tab', value='summary-tab'),
            dcc.Tab(label='raw-tab', value='raw-tab')
        ]),
        html.Div(id='block-content')

        ])

    return layout

#Both layouts are defined seperately and returned in the callback file
summary_layout = html.Div([

    dash_table.DataTable(
        id='sensor_data-table',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False}
            for i in df_summary.columns
        ],
        data=df_summary.to_dict('records'),
        filter_action="native", #Allows filtering 
        sort_action="native", #Allows sorting
        sort_mode="multi", #Sorts a single column at a time or multi columns
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

raw_layout = html.Div([

    dash_table.DataTable(
        id='sensor_data-table',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False, "format": Format(precision=4)}
            for i in df_raw.columns
        ],
        data=df_raw.to_dict('records'),
        filter_action="native", #Allows filtering 
        sort_action="native", #Allows sorting
        sort_mode="multi", #Sorts a single column at a time or multi columns
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