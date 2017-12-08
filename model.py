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
    dict_attrs = [
                  "symbol", "desc",
                  "screen_dict", "attr_dict", "history_prices", 
                  "annual_sales", "annual_incomes", 
                  "quarterly_sales", "quarterly_incomes",
                  ]

    def __init__(self, symbol):
        self.symbol = symbol
        self.desc = None
        # screen_dict includes all attributes from screen page
        # attr_dict includes all attributes from symbol detail page
        self.screen_dict = None
        self.attr_dict = None
        self.history_prices = None

        self.annual_sales = None
        self.quarterly_sales = None
        self.annual_incomes = None
        self.quarterly_incomes = None
        
        self.rsi = None
        self.ma_diff = None
        
    def to_dict(self):
        symbol_dict = {}
        for attr in self.dict_attrs:
            symbol_dict[attr] = self.__getattribute__(attr)
        return symbol_dict
    
    def from_dict(self, symbol_dict):
        for attr in self.dict_attrs:
            self.__setattr__(attr, symbol_dict[attr])
        
    def __convert_float_value(self, value_str):
        value_str = value_str.replace(',', '')
        valueSign = 1
        if value_str.startswith('(') and value_str.endswith(')'):
            value_str = value_str.strip("()")
            valueSign = -1
        if value_str[-1] in ('B', 'M', 'K'):
            value = float(value_str[:-1])
            unit = value_str[-1]
            return value * misc.get_multiplier(unit) * valueSign
        else:
            return float(value_str) * valueSign
    
    def __convert_M_value(self, num):
        num = num / 1000000
        return "%sM" % str(round(num, 2)) 
    
    def __convert_B_value(self, num):
        num = num / 1000000000
        return "%sB" % str(round(num, 2))
    
    def __convert_percent(self, float_value):
        return "{0:.1f}%".format(float_value*100)
    
    def __gen_growth(self, value_lst, as_percent=True):
        growth = []
        values = [self.__convert_float_value(v) 
                  for v in value_lst]
        for i in xrange(1, len(values)):
            change = (values[i] - values[i-1])/values[i-1]
            if as_percent:
                growth.append(self.__convert_percent(change))
            else:
                growth.append(change)
        return growth
    
    def screen_html_str(self):
        finviz_url = constants.finviz_quote_url % self.symbol
        href_str = '<tr><td><a href=\"%s\">%s</a>' % (finviz_url, 
                                                      self.symbol)
        mw_annual_url = constants.mw_annual_url % self.symbol
        mw_quarterly_url = constants.mw_quarterly_url % self.symbol
        annual_str = '<a href=\"%s\">%s</a>' % (mw_annual_url, 
                                                "Annual Stmt")
        quarterly_str = '<a href=\"%s\">%s</a>' % (mw_quarterly_url, 
                                                   "Quarterly Stmt")
        screen_attrs = ["Industry",
                        "Market", 
                        "Change", 
                        ]
        screen_str = " -- ".join(self.screen_dict[attr] for 
                               attr in screen_attrs)

        html_str = "%s (%s) (%s) -- %s</td></tr>" %(href_str, 
                                                    annual_str, 
                                                    quarterly_str,
                                                    screen_str)
        
        html_str = "%s<tr><td>%s: %s" %(html_str, "<b>Sales/e</b>",
                                        self.sales_per_employee_str())
        html_str = "%s %s: %s</td></tr>" %(html_str, "Profit/e",
                                           self.income_per_employee_str())
        return html_str
        
    def stock_watch_html_str(self):
        finviz_url = constants.finviz_quote_url % self.symbol
        href_str = '<tr><td><a href=\"%s\">%s</a>' % (
                    finviz_url, self.symbol)
        mw_annual_url = constants.mw_annual_url % self.symbol
        mw_quarterly_url = constants.mw_quarterly_url % self.symbol
        annual_str = '<a href=\"%s\">%s</a>' % (mw_annual_url, 
                                                "Annual Stmt")
        quarterly_str = '<a href=\"%s\">%s</a>' % (mw_quarterly_url, 
                                                   "Quarterly Stmt")

        html_str = "%s (%s) (%s)</td></tr>" %(href_str, 
                                              annual_str,
                                              quarterly_str)
        
        html_str = "%s<tr><td>%s: %s" %(html_str, 
                                        "<b>Sales/e</b>",
                                        self.sales_per_employee_str())
        
        html_str = "%s %s: %s</td></tr>" %(html_str, 
                                           "<b>Profit/e</b>",
                                           self.income_per_employee_str())
        
        html_str = "%s<tr><td>%s: %s (%s)" %(html_str, 
                                             "<b>Rsi</b>", 
                                             self.rsi_value(), 
                                             self.rsi_str())
        
        html_str = "%s %s: %s (%s)</td></tr>" %(html_str, 
                                                "<b>Ma_diff</b>", 
                                                self.ma_diff_value(), 
                                                self.ma_diff_str())
        
        html_str = "%s<tr><td>%s: %s" %(html_str, 
                                        "<b>Earning_date</b>",
                                        self.attr_dict['Earnings'])
        
        html_str = "%s %s: %s" %(html_str, 
                                 "<b>Perf Year</b>", 
                                 self.attr_dict['Perf Year'])
        
        html_str = "%s %s: %s </td></tr>" %(html_str, 
                                            "<b>Dividend %</b>", 
                                            self.attr_dict['Dividend %'])
        
        return html_str
    
    def fund_watch_html_str(self):
        finviz_url = constants.finviz_quote_url % self.symbol
        href_str = '<tr><td valign=\"top\"><a href=\"%s\">%s</a>' % (
                    finviz_url, self.symbol)
        
        html_str = "%s (%s)" %(href_str, self.desc)

        html_str = "%s<br>%s: %s (%s)" %(html_str, 
                                         "<b>Rsi</b>", 
                                         self.rsi_value(), 
                                         self.rsi_str())
        
        html_str = "%s<br>%s: %s (%s)" %(html_str, 
                                         "<b>Ma_diff</b>", 
                                         self.ma_diff_value(), 
                                         self.ma_diff_str())
        
        html_str = "%s<br>%s: %s" %(html_str, 
                                    "<b>Perf Year</b>",
                                    self.attr_dict['Perf Year'])

        html_str = "%s<br>%s: %s " %(html_str, 
                                     "<b>Perf Half Y %</b>", 
                                     self.attr_dict['Perf Half Y'])

        html_str = "%s<br>%s: %s" %(html_str, 
                                    "<b>Perf Quarter</b>",
                                    self.attr_dict['Perf Quarter'])
        
        html_str = "%s<br>%s: %s (%s)" %(html_str, 
                                         "<b>Relative vol</b>", 
                                         self.relative_volume(), 
                                         self.relative_volume_str())

        html_str = "%s<br>%s: %s </td>" %(html_str, 
                                          "<b>Dividend %</b>", 
                                          self.attr_dict['Dividend %'])
        
        img_src = constants.finviz_img_url % self.symbol
        html_str += '<td><img src=' + img_src
        html_str += ' width=\"60%\" height=\"60%\"/></td></tr>'
        return html_str

    def open_prices(self):
        return self.history_prices.open_prices()
        
    def close_prices(self):
        return self.history_prices.close_prices()
    
    def change(self):
        return float(self.attr_dict["Change"][:-1])
    
    def relative_volume(self):
        return float(self.attr_dict["Rel Volume"])
    
    def relative_volume_str(self):
        if self.relative_volume() > 1.2:
            return "<font color=\"green\">Above average</font>"
        if self.relative_volume() <= 1.2 and self.relative_volume() >= 0.8:
            return "<font color=\"orange\">Average</font>"
        return "<font color=\"red\">Low</font>"
    
    def sector(self):
        if self.screen_dict is not None:
            return self.screen_dict["Sector"]
        return self.attr_dict["Sector"]
    
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
        return sales / self.num_of_employee()
        
    def sales_per_employee_str(self):
        return self.__convert_M_value(self.sales_per_employee()) 

    def income_per_employee(self):
        if self.income() == '-':
            return ''
        income = self.__convert_float_value(self.income())
        return income/self.num_of_employee()
    
    def income_per_employee_str(self):
        return self.__convert_M_value(self.income_per_employee())
    
    def num_shares(self):
        return self.__convert_float_value(self.attr_dict['Shs Outstand'])
        
    def cash(self):
        if self.attr_dict['Cash/sh'] == "-":
            return 0
        cash_per_share = self.__convert_float_value(
                            self.attr_dict['Cash/sh'])
        return self.num_shares() * cash_per_share
    
    def cash_str(self):
        return self.__convert_B_value(self.cash())
    
    def cash_per_employee(self):
        return self.cash()/self.num_of_employee()
    
    def cash_per_employee_str(self):
        return self.__convert_M_value(self.cash_per_employee())
        
    def rsi_value(self):
        if self.rsi is None:
            self.rsi = metric.rsi(self.close_prices())
        return self.rsi
    
    def rsi_str(self):
        if self.rsi >= 70:
            return "<font color=\"red\">Overbought</font>"
        if self.rsi <= 30: 
            return "<font color=\"green\">Oversold</font>"
        return "<font color=\"orange\">Might be ok</font>"
        
    def ma_diff_value(self):
        if self.ma_diff is None:
            self.ma_diff = metric.ma_diff_ratio(
                                self.close_prices(), 13, 34)
        return self.ma_diff
    
    def ma_diff_str(self):
        if self.ma_diff >= 0 and self.ma_diff <= 0.01:
            return "<font color=\"green\">Good Buy</font>"
        if self.ma_diff > 0.01:
            return "<font color=\"red\">Overbought</font>"
        return "<font color=\"orange\">Negative</font>"

    def annual_sales_growth(self):
        """
        These numbers might contain errors 
        """
        return self.__gen_growth(self.annual_sales)
    
    def annual_sales_growth_trend(self):
        return metric.slope(self.__gen_growth(
                    self.annual_sales, as_percent=False))
    
    def annual_income_growth(self):
        return self.__gen_growth(self.annual_incomes)
    
    def annual_income_growth_trend(self):
        return metric.slope(self.__gen_growth(
                    self.annual_incomes, as_percent=False))
    
    def quarterly_sales_growth(self):
        return self.__gen_growth(self.quarterly_sales)

    def quarterly_sales_growth_trend(self):
        return metric.slope(self.__gen_growth(
                    self.quarterly_sales, as_percent=False))
        
    def quarterly_income_growth(self):
        return self.__gen_growth(self.quarterly_incomes)
    
    def quarterly_income_growth_trend(self):
        return metric.slope(self.__gen_growth(
                    self.quarterly_incomes, as_percent=False))
