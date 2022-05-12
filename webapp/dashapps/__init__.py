import dash
from flask_login import login_required
from flask.helpers import get_root_path

#Object to hold all the dashboard objects for easy access back in the flask app
class dash_container():

    dashboards = {}

    def add(self, name, dashboard):
        self.dashboards[name] = dashboard

    def get(self, name):
        return self.dashboards[name]

#Here we define the container object to do so
container = dash_container()

#Code to register all of our dashboards
def create_dashboards(flask_app):

    #Create attributes dashboard
    from .attributes.layout import serve_layout as attributes_serve_layout
    from .attributes.callbacks import register_callbacks as attributes_register_callbacks
    attributes_dash = register_dashapp(flask_app, 'attributes', 'settings/', attributes_serve_layout, attributes_register_callbacks)
    container.add('attributes', attributes_dash)

    #Create frost_dates dashboard
    from .frost_dates.layout import serve_layout as frost_dates_serve_layout
    from .frost_dates.callbacks import register_callbacks as frost_dates_register_callbacks
    frost_dates_dash = register_dashapp(flask_app, 'frost_dates', 'settings/frost_dates/', frost_dates_serve_layout, frost_dates_register_callbacks)
    container.add('frost_dates', frost_dates_dash)

    #Create sensor graphs dashboard
    from .sensor_graphs.layout import serve_layout as sensor_graphs_serve_layout
    from .sensor_graphs.callbacks import register_callbacks as sensor_graphs_register_callbacks
    sensor_graphs_dash = register_dashapp(flask_app, 'sensor_graphs', 'sensors/graphs/', sensor_graphs_serve_layout, sensor_graphs_register_callbacks)
    container.add('sensor_graphs', sensor_graphs_dash)

    #Create sensor data dashboard
    from .sensor_data.layout import serve_layout as sensor_data_serve_layout
    from .sensor_data.callbacks import register_callbacks as sensor_data_register_callbacks
    sensor_data_dash = register_dashapp(flask_app, 'sensor_data', 'sensors/data/', sensor_data_serve_layout, sensor_data_register_callbacks)
    container.add('sensor_data', sensor_data_dash)

    #Create calendar chart dashboard
    from .calendar_chart.layout import serve_layout as calendar_chart_serve_layout
    from .calendar_chart.callbacks import register_callbacks as calendar_chart_register_callbacks
    calendar_chart_dash = register_dashapp(flask_app, 'calendar_chart', 'calendar/chart/', calendar_chart_serve_layout, calendar_chart_register_callbacks)
    container.add('calendar_chart', calendar_chart_dash)

    #Create harvest graphs dashboard
    from .harvest_graphs.layout import serve_layout as harvest_graphs_serve_layout
    from .harvest_graphs.callbacks import register_callbacks as harvest_graphs_register_callbacks
    harvest_graphs_dash = register_dashapp(flask_app, 'harvest_graphs', 'harvest/graphs/', harvest_graphs_serve_layout, harvest_graphs_register_callbacks)
    container.add('harvest_graphs', harvest_graphs_dash)

    #Create harvest data dashboard
    from .harvest_data.layout import serve_layout as harvest_data_serve_layout
    from .harvest_data.callbacks import register_callbacks as harvest_data_register_callbacks
    harvest_data_dash = register_dashapp(flask_app, 'harvest_data', 'harvest/data/', harvest_data_serve_layout, harvest_data_register_callbacks)
    container.add('harvest_data', harvest_data_dash)

    #Create irrigation control dashboard
    from .irrigation_control.layout import serve_layout as irrigation_control_serve_layout
    from .irrigation_control.callbacks import register_callbacks as irrigation_control_register_callbacks
    irrigation_control_dash = register_dashapp(flask_app, 'irrigation_control', 'irrigation/control/', irrigation_control_serve_layout, irrigation_control_register_callbacks)
    container.add('irrigation_control', irrigation_control_dash)

#Code to register an individual dashboard
def register_dashapp(app, title, base_path, layout, register_callbacks):
    #Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial scale=1, shrink-to-fit=no"}

    #Create new instance of a dashboard
    new_dash = dash.Dash(__name__,
                        server=app,
                        url_base_pathname=f'/{base_path}',
                        assets_url_path=f'{get_root_path(__name__)}/assets/',
                        meta_tags=[meta_viewport])
    
    #Assign variables to new dash
    with app.app_context():
        new_dash.title=title
        new_dash.layout=layout
        register_callbacks(new_dash)

    #Require authentication for dash
    for view_func in new_dash.server.view_functions:
        if view_func.startswith(new_dash.config.url_base_pathname):
            new_dash.server.view_functions[view_func] = login_required(new_dash.server.view_functions[view_func])
    
    return new_dash