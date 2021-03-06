from dash import dcc, html, dash_table
import pandas as pd
from webapp.templates.app.colors import palette

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    #Have to predefine the table border as it doesn't allow string formatting
    border_color = palette['border']

    #Import the Plant database, drop the ID column
    from data.interface import get_frame, csv_to_sql
    #csv_to_sql()
    df = get_frame('Plant')
    df = df.drop('id', axis=1)
    
    layout = html.Div([
        
        dash_table.DataTable(
            id='attributes-table',
            columns=[
                {"name": "Name", "id": "name", "deletable": False, "selectable": False, "hideable": False, "type": "text"},
                {"name": "Active", "id": "active", "deletable": False, "selectable": False, "hideable": False, "type": "numeric"},
                {"name": "Indoors/Outdoors Start", "id": "start", "deletable": False, "selectable": False, "hideable": False, "type": "text"},
                {"name": "Warm/Cool Season", "id": "season", "deletable": False, "selectable": False, "hideable": False, "type": "numeric"},
                {"name": "Minimum Temperature (C)", "id": "min_temp", "deletable": False, "selectable": False, "hideable": False, "type": "numeric"},
                {"name": "Maximum Temperature", "id": "max_temp", "deletable": False, "selectable": False, "hideable": False, "type": "numeric"},
                {"name": "Spring Sow Offset", "id": "spring_sow", "deletable": False, "selectable": False, "hideable": False, "type": "numeric"},
                {"name": "Spring Transplant Offset", "id": "spring_transplant", "deletable": False, "selectable": False, "hideable": False, "type": "numeric"},
                {"name": "Fall Sow Offset", "id": "fall_sow", "deletable": False, "selectable": False, "hideable": False, "type": "numeric"},
                {"name": "Calories/Gram", "id": "cal_g", "deletable": False, "selectable": False, "hideable": False, "type": "numeric"},

            ],
            data=df.to_dict('records'),
            editable=True, #allows editing
            filter_action="native", #Allows filtering 
            sort_action="native", #Allows sorting
            sort_mode="multi", #Sorts a single column at a time or multi columns
            column_selectable="none", #Allows/disallows the selecting of rows/columns
            row_deletable=True, #Allows deletion of rows
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

            html.Button('Add Row', id='add-val', n_clicks=0),
            html.Button('Submit Changes', id='submit-val', n_clicks=0),

        ])

    return layout