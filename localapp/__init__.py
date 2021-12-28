from data import engine, init_engine

def create_localapp():

    init_engine()

    from data.interface import csv_to_sql, csv_to_sql_data, update_temp_file

    #Add plant attributes into database
    #csv_to_sql()
    #Add sensor data into database and update file table
    #csv_to_sql_data()
    #update_temp_file()

    pass

    