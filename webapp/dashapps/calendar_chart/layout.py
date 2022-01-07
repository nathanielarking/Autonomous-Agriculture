from dash import dcc, html, dash_table
import pandas as pd
from webapp.templates.app.colors import palette, tab_style, tabs_style, tab_selected_style
from datetime import datetime, date, timedelta

#Have to predefine the table border as it doesn't allow string formatting
border_color = palette['border']

#Set the start date and end date for generating the calendar
from .calendar import generate_calendar
current_date = date.today()
start_date = current_date - timedelta(days=14)
end_date = current_date + timedelta(days=180)

#Get the values for important days that will be in the columns of the table
frost_dates = pd.read_json('data/frost_dates.json')
last_frost_date = datetime.strptime(frost_dates['last_frost'][0], '%m/%d')
first_frost_date = datetime.strptime(frost_dates['first_frost'][0], '%m/%d')

last_frost_column = last_frost_date.strftime("%b %d")
first_frost_column = first_frost_date.strftime("%b %d")
current_column = current_date.strftime("%b %d")

#Import both the dataframes for planting and temps tables
df_planting, df_temps = generate_calendar(start_date, end_date)

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    layout = html.Div([

    dcc.Tabs(id='calendar-tabs', value='planting-tab', style=tabs_style, children=[
            dcc.Tab(label='Planting', value='planting-tab', style=tab_style, selected_style = tab_selected_style),
            dcc.Tab(label='Temps', value='temps-tab', style=tab_style, selected_style = tab_selected_style)
        ]),
        html.Div(id='block-content')

])
    return layout

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