from dash import dcc, html, callback_context
from dash.dependencies import Input, Output
from localapp.mqtt import activate_irrigation
from localapp import client as mqtt_client
    
def register_callbacks(dashapp):
    #Called when either of the buttons are pressed
    @dashapp.callback(Output('status', 'children'),
                      [Input('activate', 'n_clicks'),
                      Input('volume', 'value'),
                      Input('cancel', 'n_clicks')]
    )
    def update_irrigation_control(activate, volume, cancel):

        #get status from mqtt
        status = True

        changed_id = [p['prop_id'] for p in callback_context.triggered][0]

        #If the activate button was pressed
        if 'activate' in changed_id:
            activate_irrigation(mqtt_client, volume)
            print("Activated")
            status = True

        #If the cancel button was pressed
        elif 'cancel' in changed_id:
            print("cancel")
            status = False

        if status is True:
            status_div = dcc.Markdown('''Status: running''')
        else:
            status_div = dcc.Markdown('''Status: inactive''')

        return status_div

