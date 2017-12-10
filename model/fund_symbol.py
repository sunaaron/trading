'''
Created on Dec 9, 2017

@author: Aaron
'''
from model.symbol import Symbol


class FundSymbol(Symbol):

    def __init__(self, symbol):
        super(FundSymbol, self).__init__(symbol)
        self.desc = None
        
        self.fund_summary_dict = None
        self.fund_holdings_dict = None
