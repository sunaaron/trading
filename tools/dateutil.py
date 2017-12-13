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

def can_run():
    """
    As measured by UTC time (a bit tricky)
    """
    weekday = get_weekday()
    return weekday in [1, 2, 3, 4, 5]

def get_diff_days(date1, date2):
    delta = date1 - date2
    return delta.days
