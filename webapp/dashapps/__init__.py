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
    from .attributes.layout import layout as attributes_layout
    from .attributes.callbacks import register_callbacks as attributes_register_callbacks
    attributes_dash = register_dashapp(flask_app, 'Attributes', 'attributes/', attributes_layout, attributes_register_callbacks)
    container.add('attributes', attributes_dash)

    #Create harvest dashboard
    from .harvest.layout import layout as harvest_layout
    from .harvest.callbacks import register_callbacks as harvest_register_callbacks
    harvest_dash = register_dashapp(flask_app, 'Harvest', 'harvest/', harvest_layout, harvest_register_callbacks)
    container.add('harvest', harvest_dash)

#Code to register an individual dashboard
def register_dashapp(app, title, base_path, layout, register_callbacks):
    #Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial scale=1, shrink-to-fit=no"}

    #Create new instance of a dashboard
    new_dash = dash.Dash(__name__,
                        server=app,
                        url_base_pathname=f'/{base_path}',
                        assets_folder=get_root_path(__name__) + f'/{base_path}/assets/',
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