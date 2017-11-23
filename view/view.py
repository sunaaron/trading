'''
Created on Nov 11, 2017

@author: Aaron
'''
from context import constants
from tools import fetcher, parser
from ioutil import mailman

def track_fundlist():
    fetcher.fetch_watch_list_from_dropbox(constants.dropbox_fundlist_url)
    symbol_lst = parser.parse_watchlist_from_dropbox("fund.txt")
    symbol_hp_dict = fetcher.fetch_batch(symbol_lst,
                                         fetcher.fetch_historical_prices_from_pandas)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        symbol_obj.history_prices = parser.parse_historical_prices_from_pandas(
                                symbol_str, symbol_hp_dict[symbol_str])
    summary_str = mailman.gen_watchlist_fund_html(symbol_lst)
    mailman.send_email(mailman.gen_daily_watch_subject("fund"), 
                       summary_str)

def track_stocklist():
    fetcher.fetch_watch_list_from_dropbox(constants.dropbox_stocklist_url)
    symbol_lst = parser.parse_watchlist_from_dropbox("stock.txt")
    
    symbol_details_dict = fetcher.fetch_batch(symbol_lst, 
                                              fetcher.fetch_symbol_details_from_finviz)
    symbol_hp_dict = fetcher.fetch_batch(symbol_lst,
                                         fetcher.fetch_historical_prices_from_pandas)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        symbol_obj.attr_dict = parser.parse_symbol_attr_dict_from_finviz(
                                symbol_str, symbol_details_dict[symbol_str])
        symbol_obj.history_prices = parser.parse_historical_prices_from_pandas(
                                symbol_str, symbol_hp_dict[symbol_str])
    summary_str = mailman.gen_watchlist_stock_html(symbol_lst)
    mailman.send_email(mailman.gen_daily_watch_subject("stock"), 
                       summary_str)
    

def screen_new():
    screen_data = fetcher.fetch_screen_list_from_finviz()
    symbol_lst = parser.parse_screen_list_from_finviz(screen_data)
    symbol_details_dict = fetcher.fetch_batch(symbol_lst, 
                                              fetcher.fetch_symbol_details_from_finviz)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        symbol_obj.attr_dict = parser.parse_symbol_attr_dict_from_finviz(
                                symbol_str, symbol_details_dict[symbol_str])
    
    summary_str = mailman.gen_daily_summary_html(symbol_lst)
    subject = mailman.gen_daily_screen_subject(symbol_lst)
    mailman.send_email(subject, summary_str) 
