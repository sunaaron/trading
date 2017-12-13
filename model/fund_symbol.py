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
                  "desc",
                  "rsi", "ma_diff",
                  "attr_dict",
                  "summary_dict", 
                  "holdings_dict",
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
        
    def is_pick_today(self):
        """
        This relaxes the condition a bit
        """
        if self.rsi_value() >= 70:
            return False
        if self.ma_diff_value() >= 0.012:
            return False
        if self.perf_rate() < -0.1:
            return False
        if misc.to_float_value(
            self.five_year_treynor()) < 5:
            return False
        return True

    def expense_ratio(self):
        return self.summary_dict.get('Expense Ratio (net)', 'N/A')
    
    def expense_ratio_html(self):
        exp_ratio = self.expense_ratio()
        if exp_ratio == 'N/A':
            return html.orange(exp_ratio)
        expense_ratio = misc.to_float_value(exp_ratio)
        if expense_ratio >= 0.5:
            return html.red(exp_ratio)
        return html.green(exp_ratio)
    
    def net_assets(self):
        return self.summary_dict.get('Net Assets', 'N/A')
    
    def fund_pe(self):
        try:
            return misc.to_float_value(
                    self.holdings_dict['Price/Earnings']) 
        except:
            return self.holdings_dict.get('Price/Earnings', 'N/A')
    
    def fund_pe_html(self):
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
        return self.holdings_dict.get('holdings', [])
    
    def fund_perf(self, tp):
        if tp in self.perf_dict:
            return self.perf_dict[tp][0]
        return 'N/A'

    def fund_perf_category(self, tp):
        if tp in self.perf_dict:    
            return self.perf_dict[tp][1]
        return 'N/A'
    
    def five_year_beta(self):
        if not 'Beta' in self.risk_dict:
            return 'N/A'
        beta_5 = self.risk_dict['Beta']['5-year'][0]
        if beta_5 != '0':
            return beta_5
        return self.risk_dict['Beta']['3-year'][0]
   
    def five_year_treynor(self):
        if not 'Treynor Ratio' in self.risk_dict:
            return 'N/A'
        treynor_5 = self.risk_dict['Treynor Ratio']['5-year'][0] 
        if treynor_5 != '0':
            return treynor_5
        return self.risk_dict['Treynor Ratio']['3-year'][0]
        
    def treynor_html(self, value_str):
        if value_str == 'N/A':
            return value_str
        value = misc.to_float_value(value_str)
        if value > 5:
            return html.green(value_str)
        if value <= 0:
            return html.red(value_str)
        return html.orange(value_str)
