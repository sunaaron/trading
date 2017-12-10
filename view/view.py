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
from ioutil import html, mailman

def track_fundlist():
    fetcher.fetch_watch_list_from_dropbox(constants.dropbox_fundlist_url)
    symbol_lst = parser.parse_fund_watchlist_from_dropbox()
    hydrator.hydrate_fund(symbol_lst)
    summary_str = html.gen_watchlist_fund_html(symbol_lst)
    mailman.send_email(mailman.gen_daily_watch_subject("fund"), 
                       summary_str)
