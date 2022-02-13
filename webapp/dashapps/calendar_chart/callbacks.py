from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from .layout import serve_planting_layout, serve_temps_layout

def register_callbacks(dashapp):

    #Register change between tabs
    @dashapp.callback(
        Output('block-content', 'children'),
        [Input('calendar-tabs', 'value'),
        Input('start-input', 'value'),
        Input('end-input', 'value')]
    )
    def render_tables(tab, start_days, end_days):

        if start_days is None or end_days is None:
            raise PreventUpdate

        if tab =='planting-tab':
            return serve_planting_layout(start_days, end_days)

        elif tab == 'temps-tab':
            return serve_temps_layout(start_days, end_days)