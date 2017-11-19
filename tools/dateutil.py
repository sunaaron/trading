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
