from dash import dcc, html
from webapp.templates.app.colors import palette

#Layout is defined in a serve_layout function rather than on its own to ensure the data updates on page refresh. See the Live Updates section on the Dash documentation
def serve_layout():

    layout = html.Div([

        html.Div(id='status'),

        html.Div([
            html.Button('Activate', id='activate', n_clicks=0), dcc.Input(id='volume', type='number', placeholder='Liters')
        ]),

        html.Div([
            html.Button('Cancel', id='cancel', n_clicks=0)
        ])

    ])
    return layout