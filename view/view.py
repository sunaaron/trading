'''
Created on Nov 11, 2017

@author: Aaron
'''
from context import constants
from tools import (
                   fetcher, 
                   parser, 
                   hydrator, 
                   )
from ioutil import html, mailman, diskman

def track_fundlist():
    fetcher.fetch_watch_list_from_dropbox(constants.dropbox_fundlist_url)
    symbol_lst = parser.parse_fund_watchlist_from_dropbox()
    hydrator.batch_hydrate(symbol_lst, hydrator.hydrate_fund)
    summary_str = html.gen_watchlist_fund_html(symbol_lst)
    diskman.dump_symbol_lst_by_pickle(symbol_lst)
    mailman.send_email(mailman.gen_daily_watch_subject("fund"), 
                       summary_str)
