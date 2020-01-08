from add_to_sql import add_to_sql

# id from a list in crowdtangle
list_id = '554550'
past_years = [2015, 2016, 2017, 2018]
year = 2019

'''
for i in past_years:
    add_to_sql(list_id, i)
'''

add_to_sql(list_id, year)