from dash import callback_context
from dash.dependencies import Input, Output, State
import pandas as pd
from data.interface import df_to_sql, sql_to_csv

def register_callbacks(dashapp):
    #Called when either of the buttons are pressed
    @dashapp.callback(Output('attributes-table', 'data'),
                      [Input('submit-val', 'n_clicks'),
                      Input('add-val', 'n_clicks')],
                      State('attributes-table', 'data'),
                      State('attributes-table', 'columns')
    )
    def update_database(submit, add, data, cols):

        changed_id = [p['prop_id'] for p in callback_context.triggered][0]

        #If the submit button was pressed
        if 'submit-val' in changed_id:
            #Get the table data as a dataframe, push it to sql
            df = pd.DataFrame(data)
            df_to_sql(df)
            #sql_to_csv()

        #If the add button was pressed
        elif 'add-val' in changed_id:
            #Add a row
            data.append({c['id']: '' for c in cols})
        
        return data