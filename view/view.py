'''
Created on Nov 11, 2017

@author: Aaron
'''
from tools import fetcher, parser
from ioutil import mailman, diskman
from module import metric

def track_watchlist():
    fetcher.fetch_watch_list_from_dropbox()
    watchlist = parser.parse_watchlist_from_dropbox()
    
    for symbol in watchlist:
        pandas_data = fetcher.fetch_historical_prices_from_pandas(symbol)
        history_summary = parser.parse_historical_prices_from_pandas(symbol, pandas_data)
        print symbol, '\t', metric.rsi(history_summary.get_close_prices())

def screen_new():
    screen_data = fetcher.fetch_screen_list_from_finviz()
    symbol_lst = parser.parse_screen_list_from_finviz(screen_data)
    symbol_details_dict = fetcher.fetch_batch(symbol_lst, 
                                              fetcher.fetch_symbol_details_from_finviz)
    for symbol in symbol_lst:
        symbol_str = symbol.symbol
        symbol.attr_dict = parser.parse_symbol_attr_dict_from_finviz(
                                symbol_str, symbol_details_dict[symbol_str])
    
    summary_str = mailman.gen_daily_summary_html(symbol_lst)
    subject = mailman.gen_daily_subject(symbol_lst)
    mailman.send_email(subject, summary_str) 
