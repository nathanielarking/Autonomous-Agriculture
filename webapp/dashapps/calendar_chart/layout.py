from dash import dcc, html, dash_table
import pandas as pd
from data.interface import get_frost_dates
from webapp.templates.app.colors import palette, tab_style, tabs_style, tab_selected_style
from datetime import datetime, date, timedelta
from .calendars import generate_planting_calendar, generate_temps_calendar, get_date_columns

#Have to predefine the table border as it doesn't allow string formatting
border_color = palette['border']

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    layout = html.Div([

    dcc.Tabs(id='calendar-tabs', value='planting-tab', style=tabs_style, children=[
            dcc.Tab(label='Planting', value='planting-tab', style=tab_style, selected_style = tab_selected_style),
            dcc.Tab(label='Temps', value='temps-tab', style=tab_style, selected_style = tab_selected_style)
        ]),
        html.Div(id='block-content'),

    dcc.Input(id="start-input", type="number", placeholder="Past days", value=14, debounce=False, min=4, max=54, step=1, style={'marginRight':'10px'}),
    dcc.Input(id="end-input", type="number", placeholder="Future days", value=14, debounce=False, min=4, max=54, step=1),

    ])
    return layout

def serve_planting_layout(start_days, end_days):

    #Import both the dataframes for planting and temps tables
    df_planting = generate_planting_calendar(start_days, end_days)
    last_frost_column, first_frost_column, current_column = get_date_columns()

    planting_layout = html.Div([
        
        dash_table.DataTable(
            id='planting-chart',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False}
                for i in df_planting.columns
            ],
            fixed_columns={'headers': True, 'data': 1},
            style_table={'overflowX': 'auto',
                        'minWidth': '100%'},
            data=df_planting.to_dict('records'), 
            sort_action="native", #Allows sorting
            sort_mode="multi", #Sorts a single column at a time or multi columns
            column_selectable="none", #Allows/disallows the selecting of rows/columns
            page_action="native",
            page_current=0, #Default start is on first page
            page_size=150,
            style_as_list_view=False,
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': palette['col2'],
                },
                {
                    'if': {'column_id': current_column},
                    'backgroundColor': palette['col2'],
                },
                {
                    'if': {'column_id': first_frost_column},
                    'backgroundColor': palette['col4'],
                },
                {
                    'if': {'column_id': last_frost_column},
                    'backgroundColor': palette['col4'],
                },
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

    return planting_layout

def serve_temps_layout(start_day, end_day):

    #Import both the dataframes for planting and temps tables
    df_temps = generate_temps_calendar(start_day, end_day)
    last_frost_column, first_frost_column, current_column = get_date_columns()

    temps_layout = html.Div([
        
        dash_table.DataTable(
            id='temps-chart',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False}
                for i in df_temps.columns
            ],
            fixed_columns={'headers': True, 'data': 1},
            data=df_temps.to_dict('records'), 
            sort_action="native", #Allows sorting
            sort_mode="multi", #Sorts a single column at a time or multi columns
            column_selectable="none", #Allows/disallows the selecting of rows/columns
            page_action="native",
            page_current=0, #Default start is on first page
            page_size=150,
            style_table={'overflowX': 'auto',
                        'minWidth': '100%'},
            style_as_list_view=False,
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': palette['col2'],
                },
                {
                    'if': {'column_id': current_column},
                    'backgroundColor': palette['col2'],
                },
                {
                    'if': {'column_id': first_frost_column},
                    'backgroundColor': palette['col4'],
                },
                {
                    'if': {'column_id': last_frost_column},
                    'backgroundColor': palette['col4'],
                },
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

    return temps_layout