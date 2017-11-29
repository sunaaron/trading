'''
Created on Nov 11, 2017

@author: Aaron
'''
from context import constants
from tools import (
                   fetcher, 
                   parser, 
                   hydrator, 
                   filter, 
                   misc
                   )
from ioutil import mailman

def track_fundlist():
    fetcher.fetch_watch_list_from_dropbox(constants.dropbox_fundlist_url)
    symbol_lst = parser.parse_fund_watchlist_from_dropbox()
    hydrator.hydrate_medium(symbol_lst)
    symbol_lst = filter.filter_insignificant_change(symbol_lst)
    summary_str = mailman.gen_watchlist_fund_html(symbol_lst)
    mailman.send_email(mailman.gen_daily_watch_subject("fund"), 
                       summary_str)

def track_stocklist():
    fetcher.fetch_watch_list_from_dropbox(constants.dropbox_stocklist_url)
    symbol_lst = parser.parse_stock_watchlist_from_dropbox()
    hydrator.hydrate_medium(symbol_lst)
    symbol_lst = filter.filter_insignificant_change(symbol_lst)
    summary_str = mailman.gen_watchlist_stock_html(symbol_lst)
    mailman.send_email(mailman.gen_daily_watch_subject("stock"), 
                       summary_str)

def screen_daily():
    screen_data = fetcher.fetch_screen_list_from_finviz(
                    misc.build_finviz_screen_movement_url())
    symbol_lst = parser.parse_screen_list_from_finviz(screen_data)
    hydrator.hydrate_light(symbol_lst)
    symbol_lst = filter.filter_financial_sector(symbol_lst)
    summary_str = mailman.gen_daily_summary_html(symbol_lst)
    subject = mailman.gen_daily_screen_subject(symbol_lst)
    mailman.send_email(subject, summary_str) 
