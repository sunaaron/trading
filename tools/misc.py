'''
Created on Nov 11, 2017

@author: Aaron
'''
import datetime
import json

from context import constants

def get_conf():
    with open ("./conf.json", "r") as f:
        return json.loads(f.read())

def get_multiplier(unit):
    return {
        'B': 1000000000,
        'M': 1000000,
        'K': 1000,
    }[unit]
    
def to_float_value(value_str):
    value_str = value_str.replace(',', '')
    valueSign = 1
    if value_str.startswith('(') and value_str.endswith(')'):
        value_str = value_str.strip("()")
        valueSign = -1
    if value_str[-1] in ('B', 'M', 'K'):
        value = float(value_str[:-1])
        unit = value_str[-1]
        return value * get_multiplier(unit) * valueSign
    elif value_str[-1] == '%':
        return float(value_str[:-1]) * valueSign
    else:
        return float(value_str) * valueSign

def to_M_value(num):
    num = num / 1000000
    return "%sM" % str(round(num, 2)) 
    
def to_B_value(num):
    num = num / 1000000000
    return "%sB" % str(round(num, 2))

def to_percent(float_value):
    return "{0:.1f}%".format(float_value*100)

def build_finviz_screen_movement_url():
    base_url = constants.finviz_screen_url
    url_lst = base_url.split(",")
    # relative volume 1.5
    url_lst.insert(-2, "sh_relvol_o1.5")
    # trend going up
    url_lst.insert(-2, "ta_change_u")
    return ",".join(url_lst)

def timer(func):
    start_tm = datetime.datetime.now()
    func()
    end_tm = datetime.datetime.now()
    return "Completed in %d seconds" % (end_tm - start_tm).seconds
