'''
Created on Nov 24, 2017

@author: Aaron
'''
from ioutil import diskman
from tools import fetcher, parser, filter


def hydrate_with_details(symbol_lst):
    symbol_details_dict = fetcher.fetch_batch(symbol_lst, 
                            fetcher.fetch_symbol_details_from_finviz)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        symbol_obj.attr_dict = parser.parse_attr_dict_from_finviz(
                                symbol_str, symbol_details_dict[symbol_str])

def hydrate_with_historical_prices(symbol_lst):
    symbol_hp_dict = fetcher.fetch_batch(symbol_lst,
                        fetcher.fetch_historical_prices_from_pandas)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        symbol_obj.history_prices = parser.parse_historical_prices_from_pandas(
                                symbol_str, symbol_hp_dict[symbol_str])

def hydrate_with_fund_summary(symbol_lst):
    # We only use expense ratio in fund summary, so we cache them
    filtered_symbol_lst = filter.filter_local_existent(symbol_lst)
    local_symbol_dict = diskman.load_symbol_dict_by_pickle()
    symbol_summary_dict = fetcher.fetch_batch(filtered_symbol_lst,
                                fetcher.fetch_summary_from_yahoo)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        if symbol_str in local_symbol_dict:
            symbol_obj.fund_summary_dict = \
                local_symbol_dict[symbol_str].fund_summary_dict   
        else:
            symbol_obj.fund_summary_dict = parser.parse_summary_from_yahoo(
                symbol_str, symbol_summary_dict[symbol_str])
        
def hydrate_with_fund_holdings(symbol_lst):
    symbol_holdings_dict = fetcher.fetch_batch(symbol_lst,
                                fetcher.fetch_holdings_from_yahoo)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        symbol_obj.fund_holdings_dict = parser.parse_holdings_from_yahoo(
                                symbol_str, symbol_holdings_dict[symbol_str])

def hydrate_with_fund_perf(symbol_lst):
    # We only use past five years's perf in fund perf, so we cache them
    filtered_symbol_lst = filter.filter_local_existent(symbol_lst)
    local_symbol_dict = diskman.load_symbol_dict_by_pickle()
    symbol_perf_dict = fetcher.fetch_batch(filtered_symbol_lst,
                                fetcher.fetch_perf_from_yahoo)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        if symbol_str in local_symbol_dict:
            symbol_obj.fund_perf_dict = \
                local_symbol_dict[symbol_str].fund_perf_dict
        else:
            symbol_obj.fund_perf_dict = parser.parse_perf_from_yahoo(
                symbol_str, symbol_perf_dict[symbol_str])
            
def hydrate_with_annual_stmt(symbol_lst):
    symbol_annual_dict = fetcher.fetch_batch(symbol_lst, 
                            fetcher.fetch_annual_stmt_from_mw)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        res = parser.parse_stmt_from_mw(symbol_str, 
            symbol_annual_dict[symbol_str])
        symbol_obj.annual_sales = res[0]
        symbol_obj.annual_incomes = res[1]
        
def hydrate_with_quarterly_stmt(symbol_lst):        
    symbol_quarterly_dict = fetcher.fetch_batch(symbol_lst, 
                            fetcher.fetch_quarterly_stmt_from_mw)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        res = parser.parse_stmt_from_mw(symbol_str, 
                symbol_quarterly_dict[symbol_str])
        symbol_obj.quarterly_sales = res[0] 
        symbol_obj.quarterly_incomes = res[1]

def hydrate_light(symbol_lst):
    hydrate_with_details(symbol_lst)
    
def hydrate_medium(symbol_lst):
    hydrate_with_details(symbol_lst)
    hydrate_with_historical_prices(symbol_lst)
    
def hydrate_complete(symbol_lst):
    hydrate_with_details(symbol_lst)
    hydrate_with_historical_prices(symbol_lst)
    hydrate_with_annual_stmt(symbol_lst)
    hydrate_with_quarterly_stmt(symbol_lst)

def hydrate_fund(symbol_lst):
    hydrate_with_details(symbol_lst)
    hydrate_with_historical_prices(symbol_lst)
    hydrate_with_fund_summary(symbol_lst)
    hydrate_with_fund_holdings(symbol_lst)
    hydrate_with_fund_perf(symbol_lst)
    diskman.dump_symbol_dict_by_pickle(symbol_lst)
