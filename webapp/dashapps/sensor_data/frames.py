import pandas as pd
from data.interface import get_frame

def get_summary_frame():

    #Import frames and format
    df_summary = get_frame('TempFile')
    df_summary = df_summary.drop('id', axis=1)
    df_summary = df_summary.drop('group', axis=1)
    #Format columns
    df_summary['date'] = df_summary['date'].dt.date
    df_summary['min'] = df_summary['min'].map('{:,.2f}°'.format)
    df_summary['max'] = df_summary['max'].map('{:,.2f}°'.format)
    df_summary['avg'] = df_summary['avg'].map('{:,.2f}°'.format)
    df_summary.loc[:,'rate'] *= 100
    df_summary['rate'] = df_summary['rate'].map('{:,.2f}%'.format)
    df_summary.rename(columns={'date': 'Date', 'min': 'Minimim Temperature (C)', 'max': 'Maximum Temperature (C)', 'avg': 'Average Temperature (C)', 'rate': 'Data Success Rate'}, inplace=True)
    df_summary = df_summary[::-1]

    return df_summary

def get_raw_frame():

    #Import the temp reading database, drop the ID column, group column, and column containing relationship to temp file
    df_temps = get_frame('TempReading')
    df_temps = df_temps.drop('id', axis=1)
    df_temps = df_temps.drop('group', axis=1)
    df_temps = df_temps.drop('TempFile_id', axis=1)
    df_temps.rename(columns={'value': 'temp'}, inplace=True)

    #Import the moisture reading database
    df_moisture = get_frame('MoistReading')
    df_moisture = df_moisture.drop('id', axis=1)
    df_moisture['value'] = df_moisture['value'] - 200
    df_moisture['value'] = df_moisture['value'] / 1800
    df_moisture['value'] = df_moisture['value'] * 100
    df_moisture['value'] = df_moisture['value'].map('{:,.2f}'.format)
    df_moisture.rename(columns={'value': 'moisture'}, inplace=True)

    #Merge the two tables
    df_raw = pd.merge(df_temps, df_moisture, how="outer")

    #Format columns
    df_raw['temp'] = df_raw['temp'].map('{:,.2f}°'.format)
    df_raw.rename(columns={'datetime': 'Date and time', 'temp': 'Temperature (C)', 'moisture': 'Moisture (%)'}, inplace=True)
    df_raw = df_raw[::-1]

    return df_raw


