from webapp import create_webapp
from localapp import create_localapp
import logging

#Create instance of flask webapp
webapp = create_webapp()

#Contains code to be run when executed as a script (rather than imported as a module)
if __name__ == '__main__':
    #Set up basic logging
    logging.basicConfig(filename='info.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logging.info('Logging begin')

    #Run local app
    create_localapp()

    #Run flask webapp
    webapp.run(debug=True)
