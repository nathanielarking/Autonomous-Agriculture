from dash.dependencies import Input, Output, State
import pandas as pd
from webapp.templates.app.colors import palette
import plotly.express as px
from data import engine
from sqlalchemy.orm import sessionmaker
from data.models import Plant
from data.interface import get_frame
from datetime import timedelta

def register_callbacks(dashapp):
    
    #Update graph from date picker
    @dashapp.callback(
        Output('temp-graph', 'figure'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('plant-picker', 'value')
    )
    def update_range(start_date, end_date, plant_selection):

        #Get frame and drop unneccecary columns
        df = get_frame('TempFile')
        df = df.drop('id', axis=1)
        df = df.drop('group', axis=1)

        #Restrict the dataset to the range of the date picker
        df = df[df['date'].between(start_date, end_date)]
        df = df.reset_index()

        #Disconnect datapoints that have gaps more than 7 days, so that lines aren't drawn between them on the graph
        for idx, row in df.iterrows():
            if idx < len(df.index) - 1:
                delta = df.iloc[idx + 1]['date'] - df.iloc[idx]['date']
                if delta > timedelta(days=5):
                    df.loc[idx, 'date'] = None

        #Return the updated graph
        fig = px.line(df, x="date", y=df.columns[1:-1])

        #Update y axis lines and add min and max temps for plant selection
        Session = sessionmaker(bind=engine)
        with Session() as session:

            ticktext=list((range(0, 45, 2)))
            tickvals=list((range(0, 45, 2)))

            if plant_selection:
                plant = session.query(Plant).filter_by(name=plant_selection).first()
                ticktext.append(f"{plant.name} min")
                tickvals.append(plant.min_temp)
                ticktext.append(f"{plant.name} max")
                tickvals.append(plant.max_temp)

            fig.update_yaxes(
            ticktext=ticktext,
            tickvals=tickvals,
            )

        return fig

