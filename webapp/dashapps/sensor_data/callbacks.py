from dash.dependencies import Input, Output
from .layout import serve_summary_layout, serve_raw_layout

def register_callbacks(dashapp):

    #Register change between tabs
    @dashapp.callback(
        Output('block-content', 'children'),
        Input('data-tabs', 'value')
    )
    def render_tables(tab):
        if tab =='summary-tab':
            return serve_summary_layout()

        elif tab == 'raw-tab':
            return serve_raw_layout()

