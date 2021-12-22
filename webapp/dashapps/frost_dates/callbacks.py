from dash.dependencies import Input, Output, State
import pandas as pd
import json
from data.interface import df_to_sql, sql_to_csv

def register_callbacks(dashapp):
    #Called when changes are made to the table
    @dashapp.callback(Output('frost_dates_table', 'data'),
                      Input('frost_dates_table', 'data_timestamp'),
                      State('frost_dates_table', 'data')
    )
    def update_database(timestamp, data):
        #Dump the changed data into the json file

        with open('data/frost_dates.json', 'w') as file:
            json.dump(data, file)
        return data