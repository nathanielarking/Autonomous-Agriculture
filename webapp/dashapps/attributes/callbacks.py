from dash.dependencies import Input, Output, State
import pandas as pd
from data.interface import df_to_sql, sql_to_csv

def register_callbacks(dashapp):
    #Called when changes are made to the table
    @dashapp.callback(Output('attributes-table', 'data'),
                      Input('attributes-table', 'data_timestamp'),
                      State('attributes-table', 'data')
    )
    def update_database(timestamp, data):
        #Get the table data as a dataframe, push it to sql, then update the csv
        df = pd.DataFrame(data)
        df_to_sql(df)
        sql_to_csv()
        return data