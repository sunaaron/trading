'''
Created on Nov 24, 2017

@author: Aaron
'''
import time

from ioutil import diskman
from tools import fetcher, parser, filter
from tools.misc import logger

logger = logger()
local_symbol_dict = diskman.load_symbol_dict_by_pickle() 

def hydrate_with_details(symbol_lst):
    logger.info("Running hydrate_with_details")
    filtered_symbol_lst = filter.filter_local_existent_newer_than(
                                local_symbol_dict, symbol_lst, days=0)
    symbol_details_dict = fetcher.fetch_batch(filtered_symbol_lst, 
                            fetcher.fetch_symbol_details_from_finviz)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        if symbol_str in symbol_details_dict:
            symbol_obj.attr_dict = parser.parse_attr_dict_from_finviz(
                                    symbol_details_dict[symbol_str])
        else:
            symbol_obj.attr_dict = \
                local_symbol_dict[symbol_str].attr_dict
        

def hydrate_with_historical_prices(symbol_lst):
    logger.info("Running hydrate_with_historical_prices")
    filtered_symbol_lst = filter.filter_local_existent_newer_than(
                                local_symbol_dict, symbol_lst, days=0)
    symbol_hp_dict = fetcher.fetch_batch(filtered_symbol_lst,
                        fetcher.fetch_historical_prices_from_pandas)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        if symbol_str in symbol_hp_dict:
            symbol_obj.history_prices = parser.parse_historical_prices_from_pandas(
                                symbol_str, symbol_hp_dict[symbol_str])
        else:
            symbol_obj.history_prices = \
                local_symbol_dict[symbol_str].history_prices
                
def hydrate_with_fund_summary(symbol_lst):
    logger.info("Running hydrate_with_fund_summary")
    # We only use expense ratio in fund summary, so we cache them
    filtered_symbol_lst = filter.filter_local_existent_newer_than(
                                local_symbol_dict, symbol_lst, days=31)
    symbol_summary_dict = fetcher.fetch_batch(filtered_symbol_lst,
                                fetcher.fetch_summary_from_yahoo)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        if symbol_str in symbol_summary_dict:
            symbol_obj.summary_dict = parser.parse_summary_from_yahoo(
                symbol_summary_dict[symbol_str])
        else:
            symbol_obj.summary_dict = \
                local_symbol_dict[symbol_str].summary_dict
        
def hydrate_with_fund_holdings(symbol_lst):
    logger.info("Running hydrate_with_fund_holdings")
    symbol_holdings_dict = fetcher.fetch_batch(symbol_lst,
                                fetcher.fetch_holdings_from_yahoo)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        symbol_obj.holdings_dict = parser.parse_holdings_from_yahoo(
                                symbol_holdings_dict[symbol_str])

def hydrate_with_fund_perf(symbol_lst):
    logger.info("Running hydrate_with_fund_perf")
    # We only use past five years's perf in fund perf, so we cache them
    filtered_symbol_lst = filter.filter_local_existent_newer_than(
                                local_symbol_dict, symbol_lst, days=14)
    symbol_perf_dict = fetcher.fetch_batch(filtered_symbol_lst,
                                fetcher.fetch_perf_from_yahoo)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        if symbol_str in symbol_perf_dict:
            symbol_obj.perf_dict = parser.parse_perf_from_yahoo(
                symbol_perf_dict[symbol_str])
        else:
            symbol_obj.perf_dict = \
                local_symbol_dict[symbol_str].perf_dict
            
def hydrate_with_fund_risk(symbol_lst):
    logger.info("Running hydrate_with_fund_risk")
    # We only use past years's alpha,beta in fund perf, so we cache them
    filtered_symbol_lst = filter.filter_local_existent_newer_than(
                                local_symbol_dict, symbol_lst, days=14)
    symbol_risk_dict = fetcher.fetch_batch(filtered_symbol_lst,
                                fetcher.fetch_risk_from_yahoo)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        if symbol_str in symbol_risk_dict:
            symbol_obj.risk_dict = parser.parse_risk_from_yahoo(
                symbol_risk_dict[symbol_str])
        else:
            symbol_obj.risk_dict = \
                local_symbol_dict[symbol_str].risk_dict
            
def hydrate_with_annual_stmt(symbol_lst):
    logger.info("Running hydrate_with_annual_stmt")
    symbol_annual_dict = fetcher.fetch_batch(symbol_lst, 
                            fetcher.fetch_annual_stmt_from_mw)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        res = parser.parse_stmt_from_mw(
                symbol_annual_dict[symbol_str])
        symbol_obj.annual_sales = res[0]
        symbol_obj.annual_incomes = res[1]
        
def hydrate_with_quarterly_stmt(symbol_lst):
    logger.info("Running hydrate_with_quarterly_stmt") 
    symbol_quarterly_dict = fetcher.fetch_batch(symbol_lst, 
                            fetcher.fetch_quarterly_stmt_from_mw)
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        res = parser.parse_stmt_from_mw(
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
    logger.info("Running hydrate_fund, hydrating %d symbols from %s" % (
        len(symbol_lst), symbol_lst[0].symbol))
    hydrate_with_details(symbol_lst)
    hydrate_with_historical_prices(symbol_lst)
    hydrate_with_fund_summary(symbol_lst)
    hydrate_with_fund_holdings(symbol_lst)
    hydrate_with_fund_perf(symbol_lst)
    hydrate_with_fund_risk(symbol_lst)

def batch_hydrate(symbol_lst, hydrate_func, batch_size=5):
    batch_symbols = []
    for i in xrange(len(symbol_lst)):
        batch_symbols.append(symbol_lst[i])
        if (i+1)%batch_size == 0 or i == len(symbol_lst)-1:
            hydrate_func(batch_symbols)
            time.sleep(2)
            batch_symbols = []
