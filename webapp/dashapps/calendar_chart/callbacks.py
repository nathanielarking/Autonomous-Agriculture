from dash.dependencies import Input, Output
from .layout import planting_layout, temps_layout

def register_callbacks(dashapp):

    #Register change between tabs
    @dashapp.callback(
        Output('block-content', 'children'),
        Input('calendar-tabs', 'value')
    )
    def render_tables(tab):
        if tab =='planting-tab':
            return planting_layout

        elif tab == 'temps-tab':
            return temps_layout

