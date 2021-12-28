from dash.dependencies import Input, Output


def register_callbacks(dashapp):

    #Register change between tabs
    @dashapp.callback(
        Output('block-content', 'children'),
        Input('data-tabs', 'value')
    )
    def render_tables(tab):
        if tab =='summary-tab':
            return summary_layout

        elif tab == 'raw-tab':
            return raw_layout

