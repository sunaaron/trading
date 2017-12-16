'''
Created on Nov 11, 2017

@author: Aaron
'''
import os
from tools import (
                   fetcher, 
                   parser, 
                   hydrator, 
                   )
from ioutil import html, mailman, diskman

def track_fundlist(dropbox_url):
    fetcher.fetch_watch_list_from_dropbox(dropbox_url)
    filename = os.path.basename(dropbox_url)
    symbol_lst = parser.parse_fund_watchlist_from_dropbox(filename)
    hydrator.batch_hydrate(symbol_lst, hydrator.hydrate_fund)
    summary_str = html.gen_watchlist_fund_html(symbol_lst)
    diskman.dump_symbol_lst_by_pickle(symbol_lst)
    mailman.send_email(mailman.gen_daily_watch_subject("fund"), 
                       summary_str)
