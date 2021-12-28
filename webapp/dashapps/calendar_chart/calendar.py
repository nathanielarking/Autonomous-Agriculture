from data import engine
from sqlalchemy.orm import Session, sessionmaker
import pandas as pd
from data.models import Plant, TempFile

def generate_calendar(start_date, end_date):

    with Session(engine) as session:
        plants = session.query(Plant).filter_by(active=True).all()
        names = []
        for plant in plants:
            names.append(plant.name)

        datelist = pd.date_range(start_date, end_date)

        df = pd.DataFrame(columns = datelist, index = names)


        #df = df.T
        print(df)
        return df

class CalendarEntry:

    def __init__(self, plant, file):
        self.plant_name = plant.name
        self.min_temp = plant.min_temp
        self.max_temp = plant.max_temp

