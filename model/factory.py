'''
Created on Dec 9, 2017

@author: Aaron
'''
from stock_symbol import StockSymbol
from fund_symbol import FundSymbol


def gen_symbol_obj(symbol_str, symbol_type):
    if symbol_type == "fund":
        return FundSymbol(symbol_str)
    return StockSymbol(symbol_str)
