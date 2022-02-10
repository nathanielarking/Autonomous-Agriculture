#Same code as normal main but it only starts the localapp

from localapp import localapp_thread
import logging
from threading import Thread

#Contains code to be run when executed as a script (rather than imported as a module)
if __name__ == '__main__':
    #Set up basic logging
    logging.basicConfig(filename='info.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logging.info('Logging begin')

    #Initialize thread to run the mqtt local application
    localapp_thread = Thread(target=localapp_thread)
    localapp_thread.start()