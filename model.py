'''
Created on Nov 11, 2017

@author: Aaron
'''
from context import constants
from module import metric
from tools import misc

class DailySummary(object):
    def __init__(self, dt, op, cp, vol):
        self.date = dt
        self.open = op
        self.close = cp
        self.volume = vol
        
    def __str__(self):
        return str(self.date)[:10] + '\t' + str(
                self.open) + '\t' + str(
                self.close) + '\t' +  str(
                self.volume)

class HistorySummary(object):
    
    def __init__(self, symbol, d_sums):
        self.symbol = symbol
        self.daily_summaries = d_sums
        
    def __str__(self):
        out_str = self.symbol + "\n"
        for ds in self.daily_summaries:
            out_str += str(ds) + '\n'
        return out_str.rstrip('\n')
    
    def close_prices(self):
        return [ds.close for ds in self.daily_summaries] 
    
    def open_prices(self):
        return [ds.open for ds in self.daily_summaries]

class Symbol(object):
    
    def __init__(self, symbol):
        self.symbol = symbol
        # screen_dict includes all attributes from screen page
        # attr_dict includes all attributes from symbol detail page
        self.screen_dict = None
        self.attr_dict = None
        self.history_prices = None
        
        self.rsi = None
        self.ma_diff = None
    
    def __convert_float_value(self, value_str):
        value = float(value_str[:-1])
        unit = value_str[-1]
        return value * misc.get_multiplier(unit)
    
    def __convert_M_value(self, num):
        num = num / 1000000
        return "%sM" % str(round(num, 2)) 
        
    def screen_html_str(self):
        finviz_url = constants.finviz_quote_url % self.symbol
        href_str = '<tr><td><a href=\"%s\">%s</a>' % (finviz_url, 
                                              self.symbol)
        reuters_url = constants.reuters_financial_url % self.symbol
        reuters_str = '<a href=\"%s\">%s</a>' % (reuters_url, 
                                                 "financials")
        screen_attrs = ["Industry",
                        "Market", 
                        "Change", 
                        ]
        screen_str = " -- ".join(self.screen_dict[attr] for 
                               attr in screen_attrs)

        html_str = "%s (%s) -- %s</td></tr>" %(href_str, 
                                              reuters_str, 
                                              screen_str)
        
        html_str = "%s<tr><td>%s: %s" %(html_str, "<b>Sales/e</b>",
                                        self.sales_per_employee())
        html_str = "%s %s: %s</td></tr>" %(html_str, "Profit/e",
                                           self.income_per_employee())
        return html_str
        
    def stock_watch_html_str(self):
        finviz_url = constants.finviz_quote_url % self.symbol
        href_str = '<tr><td><a href=\"%s\">%s</a>' % (
                    finviz_url, self.symbol)
        reuters_url = constants.reuters_financial_url % self.symbol
        reuters_str = '<a href=\"%s\">%s</a>' % (reuters_url, 
                                                 "financials")

        html_str = "%s (%s)</td></tr>" %(href_str, reuters_str)
        
        html_str = "%s<tr><td>%s: %s" %(html_str, 
                                        "<b>Sales/e</b>",
                                        self.sales_per_employee())
        
        html_str = "%s %s: %s</td></tr>" %(html_str, 
                                           "<b>Profit/e</b>",
                                           self.income_per_employee())
        
        html_str = "%s<tr><td>%s: %s (%s)" %(html_str, 
                                             "<b>Rsi</b>", 
                                             self.rsi_value(), 
                                             self.rsi_str())
        
        html_str = "%s %s: %s (%s)</td></tr>" %(html_str, 
                                                "<b>Ma_diff</b>", 
                                                self.ma_diff_value(), 
                                                self.ma_diff_str())
        
        html_str = "%s<tr><td>%s: %s</td></tr>" %(html_str, 
                                                  "<b>Earning_date</b>",
                                                  self.attr_dict['Earnings'])
        return html_str
    
    def fund_watch_html_str(self):
        finviz_url = constants.finviz_quote_url % self.symbol
        href_str = '<tr><td><a href=\"%s\">%s</a>' % (
                    finviz_url, self.symbol)

        html_str = "%s<tr><td>%s: %s (%s)" %(href_str, 
                                             "<b>Rsi</b>", 
                                             self.rsi_value(), 
                                             self.rsi_str())
        
        html_str = "%s %s: %s (%s)</td></tr>" %(html_str, 
                                                "<b>Ma_diff</b>", 
                                                self.ma_diff_value(), 
                                                self.ma_diff_str())
        return html_str

    def open_prices(self):
        return self.history_prices.open_prices()
        
    def close_prices(self):
        return self.history_prices.close_prices()
    
    def sales(self):
        return self.attr_dict['Sales']
    
    def income(self):
        return self.attr_dict['Income']

    def num_of_employee(self):
        return int(self.attr_dict['Employees'])
    
    def sales_per_employee(self):
        if self.sales() == '-':
            return ''
        sales = self.__convert_float_value(self.sales())
        sales_per_employee = sales / self.num_of_employee()
        return self.__convert_M_value(sales_per_employee) 

    def income_per_employee(self):
        if self.income() == '-':
            return ''
        income = self.__convert_float_value(self.income())
        income_per_employee = income/self.num_of_employee()
        return self.__convert_M_value(income_per_employee)
    
    def rsi_value(self):
        if self.rsi is None:
            self.rsi = metric.rsi(self.close_prices())
        return self.rsi
    
    def rsi_str(self):
        if self.rsi >= 70:
            return "<font color=\"red\">Overbought</font>"
        if self.rsi <= 30: 
            return "<font color=\"green\">Good Buy</font>"
        return "<font color=\"orange\">Might be ok</font>"
        
    def ma_diff_value(self):
        if self.ma_diff is None:
            self.ma_diff = metric.ma_diff_ratio(
                                self.close_prices(), 13, 34)
        return self.ma_diff
    
    def ma_diff_str(self):
        if self.ma_diff >= 0 and self.ma_diff <= 0.0075:
            return "<font color=\"green\">Good Buy</font>"
        if self.ma_diff > 0.0075:
            return "<font color=\"red\">Overbought</font>"
        return "<font color=\"orange\">Might be ok</font>"
