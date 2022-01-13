from webapp import create_webapp
from localapp import run_localapp
import logging
import threading

#Create instance of flask webapp
webapp = create_webapp()

#Contains code to be run when executed as a script (rather than imported as a module)
if __name__ == '__main__':
    #Set up basic logging
    logging.basicConfig(filename='info.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logging.info('Logging begin')

    #Initialize thread to run the mqtt local application
    localapp_thread = threading.Thread(target=run_localapp)
    localapp_thread.start()

    #Initialize thread to run the flask web application
    webapp.run(debug=False)