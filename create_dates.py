import arrow


'''Create daily dates for a given year 

    Args:
        year (int)

    Returns:
        list with days

    '''


def create_dates(year):
    # last day is always the day before

    date_now = arrow.now()    
    date_yesterday = arrow.now().replace(days=-1)
    date_start = arrow.get(year, 1, 1)

    # create dates for current year
    if date_now.year == year:
        date_end = date_yesterday
    else:
        date_end = arrow.get(year, 12, 31)

    dates = arrow.Arrow.range('day', date_start, date_end)

    r = list()
    for i in dates:
        t = i.format('YYYY-MM-DD')
        r.append(t)

    return r