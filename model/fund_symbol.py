'''
Created on Dec 9, 2017

@author: Aaron
'''
from tools import misc
from ioutil import html
from model.symbol import Symbol


class FundSymbol(Symbol):

    def __init__(self, symbol):
        super(FundSymbol, self).__init__(symbol)
        self.desc = None
        
        self.fund_summary_dict = None
        self.fund_holdings_dict = None

    def expense_ratio(self):
        return self.fund_summary_dict['Expense Ratio (net)']
    
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
            return html.green("Normal")
        if pe >= 50:
            return html.red("Too High")
        if pe >= 35 and pe < 50: 
            return html.orange("High")
        return html.green("Normal")
    
    def holdings(self):
        return self.fund_holdings_dict['holdings']
