'''
Created on Nov 11, 2017

@author: Aaron
'''
from tools import fetcher, parser
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
    print symbol_lst

