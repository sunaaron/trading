'''
Created on Nov 10, 2017

@author: Aaron
'''
from datetime import datetime, timedelta
import os
import requests
import time
from threading import Thread
import urllib2

from context import constants
from tools import misc
from tools.misc import retry
 
from pandas_datareader import data, wb
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from subprocess import call

conf = misc.get_conf()

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_screen_list_from_finviz(finviz_screen_url):
    return urllib2.urlopen(finviz_screen_url).read()

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_symbol_details_from_finviz(symbol_str):
    url = constants.finviz_quote_url % symbol_str
    return urllib2.urlopen(url).read()

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_summary_from_bbg(symbol_str):
    url = constants.bbg_quote_url % symbol_str
    return urllib2.urlopen(url).read()
    
@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_markets_from_cnn():
    hp_url = constants.cnn_markets_url
    return urllib2.urlopen(hp_url).read()
    
@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_summary_from_yahoo(symbol_str):
    hp_url = constants.yahoo_q_url % symbol_str
    return urllib2.urlopen(hp_url).read()

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_holdings_from_yahoo(symbol_str):
    hp_url = constants.yahoo_holdings_url % symbol_str
    return urllib2.urlopen(hp_url).read()

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_perf_from_yahoo(symbol_str):
    hp_url = constants.yahoo_perf_url % symbol_str
    return urllib2.urlopen(hp_url).read()

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_risk_from_yahoo(symbol_str):
    hp_url = constants.yahoo_risk_url % symbol_str
    return urllib2.urlopen(hp_url).read()

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_historical_prices_from_yahoo(symbol_str):
    hp_url = constants.yahoo_hp_url % symbol_str
    return urllib2.urlopen(hp_url).read()

@retry(requests.exceptions.ConnectionError, tries=3, delay=3, backoff=2)
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
    
@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_annual_stmt_from_mw(symbol_str):
    url = constants.mw_annual_url % symbol_str
    return urllib2.urlopen(url).read()

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def fetch_quarterly_stmt_from_mw(symbol_str):
    url = constants.mw_quarterly_url % symbol_str
    return urllib2.urlopen(url).read()

def fetch_and_store(symbol_str, symbol_dict, func):
    symbol_dict[symbol_str] = func(symbol_str)
    
def fetch_batch(symbol_lst, func):
    symbol_dict = {}

    thread_lst = []
    for symbol_obj in symbol_lst:
        t = Thread(target = fetch_and_store, 
                   args = (symbol_obj.symbol, 
                           symbol_dict,
                           func,
                           ))
        thread_lst.append(t)
        t.start()
 
    for t in thread_lst:
        t.join()    
    return symbol_dict
