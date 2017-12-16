'''
Created on Nov 11, 2017

@author: Aaron
'''
import datetime
from functools import wraps
import json
import logging
import time


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

def timer(func, *args):
    start_tm = datetime.datetime.now()
    func(*args)
    end_tm = datetime.datetime.now()
    return "Completed in %d seconds" % (end_tm - start_tm).seconds

def logger():
    logger = logging.getLogger('trading')
    logger.setLevel(logging.DEBUG)
    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - \
        %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    return logger

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry