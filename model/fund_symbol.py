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
                  "summary_dict", 
                  "perf_dict",
                  "risk_dict",
                  ]

    def __init__(self, symbol):
        super(FundSymbol, self).__init__(symbol)
        self.symbol_type = "fund"
        self.desc = None
        
        self.summary_dict = None
        self.holdings_dict = None
        self.perf_dict = None
        self.risk_dict = None

    def expense_ratio(self):
        return self.summary_dict['Expense Ratio (net)']
    
    def expense_ratio_str(self):
        exp_ratio = self.expense_ratio()
        if exp_ratio == 'N/A':
            return html.orange(exp_ratio)
        expense_ratio = misc.to_float_value(exp_ratio)
        if expense_ratio >= 0.5:
            return html.red(exp_ratio)
        return html.green(exp_ratio)
    
    def net_assets(self):
        return self.summary_dict['Net Assets']
    
    def fund_pe(self):
        try:
            return misc.to_float_value(
                    self.holdings_dict['Price/Earnings']) 
        except:
            return self.holdings_dict.get('Price/Earnings', 'N/A')
    
    def fund_pe_str(self):
        pe = self.fund_pe()
        pe_str = self.holdings_dict.get('Price/Earnings', 'N/A')
        if pe == 'N/A':
            return html.orange(pe)
        if pe >= 50:
            return html.red(pe_str)
        if pe >= 35 and pe < 50: 
            return html.orange(pe_str)
        return html.green(pe_str)
    
    def holdings(self):
        return self.holdings_dict['holdings']
    
    def fund_perf(self, tp):
        if tp in self.perf_dict:
            return self.perf_dict[tp][0]
        return 'N/A'

    def fund_perf_category(self, tp):
        if tp in self.perf_dict:    
            return self.perf_dict[tp][1]
        return 'N/A'
    
    def three_year_beta(self):
        if 'Beta' in self.risk_dict:
            if '3-year' in self.risk_dict['Beta']:
                return self.risk_dict['Beta']['3-year'][0]
        return 'N/A'
   
    def three_year_beta_category(self):
        if 'Beta' in self.risk_dict:
            if '3-year' in self.risk_dict['Beta']:
                return self.risk_dict['Beta']['3-year'][1]
        return 'N/A'