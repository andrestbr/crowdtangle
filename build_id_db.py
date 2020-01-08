import json
import pandas as pd
import requests

from pandas import Series, DataFrame

"""Create a csv file with the ids of the Facebook accounts in the list dw_all.

    Args:
        list_id (int): Id of the list dw_all

    Returns:
        bolean: True for succes, False otherwise
"""


def build_id_db(list_id):

    end_point = 'leaderboard'
    api_url = 'https://api.crowdtangle.com/' + end_point
    api_key = 'w66FiQJdskeVj0JyiFFwVLBT72215hvSsvytnfdG'
    end_date = '2017-06-10'

    # initiate session object s
    s = requests.Session()

    # use method get to request the page data from the api
    # store the results in the variable r
    r = s.get(api_url, params={'listId':list_id, 'endDate':end_date, 'count':100}, headers=({'Content-Type':'application/json', 'x-api-token':api_key}))

    # stores the json values in a dictionary
    r_dictionary = json.loads(r.text)

    accounts = r_dictionary['result']['accountStatistics']

    accounts_list = {}
    length = len(accounts)

    # create dictionary with name of the account and id
    for i in range(length):
        name = accounts[i]['account']['handle']
        id = accounts[i]['account']['id']

        accounts_list[name] = id

    df = Series(accounts_list)
    print(df)

    df.to_csv('fb_account_ids.csv', sep=';', header=False, mode='w')

    return True
