from dash import dcc, html, dash_table
from dash.dash_table.Format import Format
import pandas as pd
from webapp.templates.app.colors import palette, tab_style, tabs_style, tab_selected_style
from datetime import datetime

#Have to predefine the table border as it doesn't allow string formatting
border_color = palette['border']

from .frames import get_summary_frame, get_raw_frame

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    layout = html.Div([

        dcc.Tabs(id='data-tabs', value='summary-tab', style=tabs_style, children=[
            dcc.Tab(label='Summary', value='summary-tab', style=tab_style, selected_style = tab_selected_style),
            dcc.Tab(label='Hourly', value='raw-tab', style=tab_style, selected_style = tab_selected_style)
        ]),
        html.Div(id='block-content')

        ])

    return layout

#Both layouts are defined seperately and returned in the callback file
def serve_summary_layout():

    #Import the tempfile database
    df_summary = get_summary_frame()

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

    return summary_layout

def serve_raw_layout():
    
    #Import the tempfile database
    df_raw = get_raw_frame()

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

    return raw_layout