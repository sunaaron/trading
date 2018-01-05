'''
Created on Nov 19, 2017

@author: Aaron
'''
import datetime

def get_today_date():
    return datetime.date.today()

def get_year_month():
    now = datetime.datetime.now()
    return "%s-%s" %(now.year, '{:02d}'.format(now.month))

def get_weekday():
    """
    Monday is 0, and Sunday is 6
    """
    return datetime.datetime.today().weekday()

def get_last_week_range():
    # weekdays only, and the output range only covers 5 days
    weekday = get_weekday()
    start_delta = datetime.timedelta(days=weekday, weeks=1)
    start_day = get_today_date() - start_delta
    end_delta = datetime.timedelta(days=4)
    end_day = start_day + end_delta
    return (start_day, end_day)

def get_last_week_range_as_str():
    start_day, end_day = get_last_week_range()
    return (str(start_day), str(end_day))

def get_last_month():
    first_day = get_today_date().replace(day=1)
    lastMonth = first_day - datetime.timedelta(days=1)
    return (lastMonth.year, lastMonth.month)

def can_run():
    """
    As measured by UTC time (a bit tricky)
    """
    weekday = get_weekday()
    return weekday in [1, 2, 3, 4, 5]

def get_diff_days(date1, date2):
    delta = date1 - date2
    return delta.days
