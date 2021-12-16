from dash import dcc, html

layout = html.Div([
    html.H1('Attributes'),
    dcc.Dropdown(
        id='my_dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],
        value='COKE'
    ),
    dcc.Graph(id='my-graph')
], style={'width': '900'})