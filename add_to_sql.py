import pandas as pd
import sqlite3
import pandas.io.sql as sql
import time
import subprocess
import platform

from pandas import Series, DataFrame
from get_all_accounts import get_all_accounts
from create_dates import create_dates

'''Add year to a table in a sql database.
'''


def add_date_as_index(df, date):
    '''
    Add date as an index to a dataframe.

    '''

    # create a column with the given date on every row
    df['date'] = date

    # set date column as index
    # set_index(inplace=True) could work as well
    df = df.set_index('date')
    return df


def get_dates_from_sql(sql_name, table_name):
    dates_in_db = list()
    con = sqlite3.connect(sql_name)
    c = con.cursor()
    
    try:
        c.execute('''SELECT date FROM {0}'''.format(table_name))
    except sqlite3.OperationalError as err:
        return err
    
    r = c.fetchall()

    # r has all the dates in the database
    for i in r:
        dates_in_db.append(i[0])

    dates_unique = Series(dates_in_db).unique()
    con.close()
    return dates_unique


def add_to_sql(list_id, year):
    '''Add year to a table in a sql database.

    Args:
        list_id (int): id from a list in crowdtangle
        year (int): year to add

    Returns: True
    '''

    # check if code is running in windows or macos
    if platform.system() != "Windows":
        subprocess.Popen('caffeinate -d', shell=True)     
    
    dates = create_dates(year)
    sql_name = 'db/fb_' + str(year) + '.db'
    table_name = 'fb_' + str(year)
    
    con = sqlite3.connect(sql_name)
    c = con.cursor()
    
    # add first dataframe
    status, df_all_accounts = get_all_accounts(list_id, dates[0])
    print('add first dataframe')
    
    # get_all_accounts returns True and a DataFrame
    if status:
        # the DataFrame object is given as the second argument
        # add date as the index to the dataframe
        data = add_date_as_index(df_all_accounts, dates[0])
        try:
            data.to_sql(table_name, con, if_exists='fail', index=True)
        except ValueError as err:
            print(err)
            pass

    for i in dates:
        
        dates_in_db = get_dates_from_sql(sql_name, table_name)
        if i not in dates_in_db:
        
            status, df_all_accounts = get_all_accounts(list_id, i)
            time.sleep(12)
            print(f'try current date: {i}')
            print(status)
        
            # get_all_accounts returns True and a DataFrame
            if status:
            
                # the DataFrame object is given as the second argument
                data = add_date_as_index(df_all_accounts, i)

                df = sql.read_sql('SELECT * FROM fb_{0}'.format(str(year)), con, index_col='date')
                df = df.append(data)
            
                df.to_sql(table_name, con, if_exists='replace', index=True)
                print(i)

            else:
                print('date ' + i + ' could not be retrieved')
                # check if code is running in windows or macos
                if platform.system() != "Windows":
                    subprocess.run('killall caffeinate', shell=True)
                
                return False

    # check if code is running in windows or macos
    if platform.system() != "Windows":
        subprocess.run('killall caffeinate', shell=True)
    
    con.close()
    return True
