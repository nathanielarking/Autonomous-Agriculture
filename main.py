from webapp import create_app
import logging

#Create instance of flask webapp
app = create_app()

#Contains code to be run when executed as a script (rather than imported as a module)
if __name__ == '__main__':
    #Set up basic logging
    logging.basicConfig(filename='info.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logging.info('Logging begin')

    #Run flask webapp
    app.run(debug=True)
