'''
Created on Nov 11, 2017

@author: Aaron
'''
import os

from context import constants
from ioutil import html, mailman, diskman
from tools import (
                   fetcher, 
                   parser, 
                   hydrator, 
                   )

def track_fundlist(dropbox_url):
    # fetch markets changes
    markets_content = fetcher.fetch_markets_from_cnn()
    index_dict = parser.parse_markets_from_cnn(markets_content)
    
    # fetch symbols
    fetcher.fetch_watch_list_from_dropbox(dropbox_url)
    filename = os.path.basename(dropbox_url)
    symbol_lst = parser.parse_fund_watchlist_from_dropbox(filename)
    hydrator.batch_hydrate(symbol_lst, hydrator.hydrate_fund)
    summary_str = html.gen_watchlist_fund_html(symbol_lst, index_dict)
    diskman.dump_symbol_lst_by_pickle(symbol_lst)
    mailman.send_email(mailman.gen_daily_watch_subject("fund"), 
                       summary_str)

def track_correlation():
    dropbox_url = constants.dropbox_coef_url
    fetcher.fetch_watch_list_from_dropbox(dropbox_url)
    coef_lst = parser.parse_coef_list_from_dropbox()
    summary_str = html.gen_correlation_html(coef_lst)
    mailman.send_email(mailman.gen_correlation_subject(), 
                       summary_str)

    