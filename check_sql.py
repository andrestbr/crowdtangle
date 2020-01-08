import arrow
import pandas as pd
import pandas.io.sql as sql
import sqlite3

from pandas import DataFrame, Series

from create_dates import create_dates

con = sqlite3.connect('db/fb_2018.db')

c = con.cursor()


c.execute('''SELECT date FROM fb_2018''')

r = c.fetchall()

# years in the database
dates = list()
for i in r:
    dates.append(arrow.get(i[0]).format('YYYY-MM-DD'))

print('number of rows:', len(r))
dates_unique = Series(dates).unique()
print('dates in the database:', dates_unique)
print('number of dates in the database:', len(dates_unique))


# check if every date has every account
for i in dates_unique:
    c.execute('''SELECT name FROM fb_2018 WHERE date LIKE (?)''', (i, ))

    r = c.fetchall()


    names = list()
    for j in r:
        names.append(j[0])

    if len(Series(names).unique()) != 74:
        print('date ', i, 'by', len(Series(names).unique()))


year = 2018
df = sql.read_sql('SELECT * FROM fb_{0}'.format(str(year)), con, index_col='date')

df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M')

df_year = df.loc[df.index.year == year]

df_month = df_year.loc[df_year.index.month == 6]

df_day = df_month.loc[df_month.index.day == 18]

print(df_day.isnull().count())

print(df_day)

length = 74
dates = create_dates(2018)

for i in dates:
    d = df.loc[i].isnull().count()
    for j in d:
        if j != length:
            print('dif')
        

con.commit()
con.close()
