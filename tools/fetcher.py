'''
Created on Nov 10, 2017

@author: Aaron
'''
from datetime import datetime, timedelta
import os
import time
from threading import Thread
import requests
import urllib2

from context import constants
from tools import misc
 
from pandas_datareader import data, wb
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from subprocess import call

conf = misc.get_conf()

def fetch_screen_list_from_finviz():
    return urllib2.urlopen(constants.finviz_screen_url).read()

def fetch_symbol_details_from_finviz(symbol_str):
    url = constants.finviz_quote_url % symbol_str
    return urllib2.urlopen(url).read()

def fetch_historical_prices_from_yahoo(symbol_str):
    hp_url = constants.yahoo_hp_url % symbol_str
    return urllib2.urlopen(hp_url).read()

def fetch_historical_prices_from_pandas(symbol_str):
    requests.packages.urllib3.disable_warnings()
    date_diff = timedelta(days=365)
    return data.DataReader(symbol_str, 'yahoo', datetime.today()-date_diff, 
                           datetime.today())

def fetch_watch_list_from_dropbox(dropbox_url):
    basename = os.path.basename(dropbox_url)
    if os.path.exists(basename):
        os.unlink(basename)
    call(["wget", dropbox_url])

def fetch_and_store(symbol_str, symbol_dict, func):
    symbol_dict[symbol_str] = func(symbol_str)
    
def fetch_batch(symbol_lst, func):
    symbol_dict = {}
    batch_size = int(conf['fetch_batch_size'])

    thread_lst = []
    count = 0
    for symbol_obj in symbol_lst:
        t = Thread(target = fetch_and_store, 
                   args = (symbol_obj.symbol, 
                           symbol_dict,
                           func,
                           ))
        thread_lst.append(t)
        t.start()
        count += 1
        if batch_size > 0 and count % batch_size == 0:
            time.sleep(5)
 
    for t in thread_lst:
        t.join()    
    return symbol_dict