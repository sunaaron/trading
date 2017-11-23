'''
Created on Nov 19, 2017

@author: Aaron
'''
import datetime

def get_today_date():
    return datetime.date.today()

def get_year_month():
    now = datetime.datetime.now()
    return "%s-%s" %(now.year, now.month)

def get_weekday():
    """
    Monday is 0, and Sunday is 6
    """
    return datetime.datetime.today().weekday()

def can_do_screen():
    weekday = get_weekday()
    return weekday in [0, 1, 2, 3, 4]

def can_do_stock_track():
    weekday = get_weekday()
    return weekday in [0, 2, 4]

def can_do_fund_track():
    weekday = get_weekday()
    return weekday in [1, 3]
