from dash.dependencies import Input, Output, State
import pandas as pd
import json
from data.interface import df_to_sql, sql_to_csv, frost_to_json

def register_callbacks(dashapp):

    #Called when the submit button is pressed 
    @dashapp.callback(Output('frost_dates_table', 'data'),
                      Input('submit-val', 'n_clicks'),
                      State('frost_dates_table', 'data')
    )
    def update_database(submit, data):
        
        #Dump the changed data into the json file
        if submit > 0:
            frost_to_json(data)

        return data