'''
Created on Nov 19, 2017

@author: Aaron
'''
import os
from tools import dateutil

def get_year_month_path():
    year_month_str = dateutil.get_year_month()
    year_month_path = "./data/%s" % year_month_str
    if not os.path.exists(year_month_path):
        os.mkdir(year_month_path)
    return year_month_path

