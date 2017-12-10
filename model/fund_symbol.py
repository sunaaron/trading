'''
Created on Dec 9, 2017

@author: Aaron
'''
from tools import misc
from ioutil import html
from model.symbol import Symbol


class FundSymbol(Symbol):
    dict_attrs = [
                  "symbol", "symbol_type",
                  "fund_summary_dict", 
                  "fund_perf_dict",
                  ]

    def __init__(self, symbol):
        super(FundSymbol, self).__init__(symbol)
        self.symbol_type = "fund"
        self.desc = None
        
        self.fund_summary_dict = None
        self.fund_holdings_dict = None
        self.fund_perf_dict = None

    def expense_ratio(self):
        return self.fund_summary_dict['Expense Ratio (net)']
    
    def expense_ratio_str(self):
        expense_ratio = misc.to_float_value(self.expense_ratio())
        if expense_ratio >= 0.5:
            return html.red(self.expense_ratio())
        return html.green(self.expense_ratio())
    
    def net_assets(self):
        return self.fund_summary_dict['Net Assets']
    
    def fund_pe(self):
        try:
            return misc.to_float_value(
                    self.fund_holdings_dict['Price/Earnings']) 
        except:
            return self.fund_holdings_dict.get('Price/Earnings', 'N/A')
    
    def fund_pe_str(self):
        pe = self.fund_pe()
        if pe == 'N/A':
            return html.orange(pe)
        if pe >= 50:
            return html.red(self.fund_holdings_dict['Price/Earnings'])
        if pe >= 35 and pe < 50: 
            return html.orange(self.fund_holdings_dict['Price/Earnings'])
        return html.green(self.fund_holdings_dict['Price/Earnings'])
    
    def holdings(self):
        return self.fund_holdings_dict['holdings']
        