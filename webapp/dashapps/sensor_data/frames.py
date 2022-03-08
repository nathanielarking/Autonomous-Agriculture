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
    df_raw = get_frame('TempReading')
    df_raw = df_raw.drop('id', axis=1)
    df_raw = df_raw.drop('group', axis=1)
    df_raw = df_raw.drop('TempFile_id', axis=1)
    #Format columns
    df_raw['value'] = df_raw['value'].map('{:,.2f}°'.format)
    df_raw.rename(columns={'datetime': 'Date and time', 'value': 'Temperature (C)'}, inplace=True)
    df_raw = df_raw[::-1]

    return df_raw


