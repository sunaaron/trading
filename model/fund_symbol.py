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
                  "history_prices",
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
        if self.rsi_value() >= 65:
            return False
        if self.ma_rally_days() < 3:
            return False
        # Miss the train
        if self.ma_rally_days() > 20:
            return False
        if self.ma_rally_gain() > 0.035:
            return False
        if self.ma_diff_trend() <= 0:
            return False
        if self.perf_trend_since_year() <= -0.02:
            return False
        if self.perf_trend_since_half_year() <= -0.02:
            return False
        if self.price_below_ma200():
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
        if expense_ratio >= 0.4:
            return html.orange(exp_ratio)
        return html.green(exp_ratio)
    
    def net_assets(self):
        return self.summary_dict.get('Net Assets', 'N/A')
    
    def net_assets_html(self):
        ast_str = self.net_assets()
        if ast_str.endswith('B'):
            return html.green(ast_str)
        if ast_str.endswith('M'):
            ast_value = float(ast_str[:-1])
            if ast_value <= 100:
                return html.red(ast_str)
            if ast_value > 100 and ast_value <= 300:
                return html.orange(ast_str)
            return html.green(ast_str)
        return html.red(ast_str)
    
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
        if pe >= 40:
            return html.red(pe_str)
        if pe >= 30 and pe < 40: 
            return html.orange(pe_str)
        return html.green(pe_str)
    
    def holdings(self):
        return self.holdings_dict.get('holdings', [])
    
    def fund_perf(self, tp):
        if tp == '1-Year':
            if self.attr_dict['Perf Year'] == '-':
                return self.attr_dict['Perf YTD']
            return self.attr_dict['Perf Year']
        if tp in self.perf_dict:
            return self.perf_dict[tp][0]
        return 'N/A'

    def five_year_risk_factor(self, name):
        if not name in self.risk_dict:
            return 'N/A'
        value = self.risk_dict[name]['5-year'][0]
        if value != '0':
            return value
        return self.risk_dict[name]['3-year'][0]
    
    def five_year_alpha(self):
        return self.five_year_risk_factor('Alpha')
    
    def five_year_beta(self):
        return self.five_year_risk_factor('Beta')
   
    def five_year_treynor(self):
        return self.five_year_risk_factor('Treynor Ratio')
        
    def treynor_html(self, value_str):
        if value_str == 'N/A':
            return value_str
        value = misc.to_float_value(value_str)
        if value > 5:
            return html.green(value_str)
        if value <= 0:
            return html.red(value_str)
        return html.orange(value_str)
