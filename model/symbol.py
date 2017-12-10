'''
Created on Nov 11, 2017

@author: Aaron
'''
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
        self.attr_dict = None
        self.history_prices = None
        
        self.rsi = None
        self.ma_diff = None

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
            return "<font color=\"green\">Above Average</font>"
        if self.relative_volume() <= 1.2 and self.relative_volume() >= 0.8:
            return "<font color=\"orange\">Average</font>"
        return "<font color=\"red\">Below Average</font>"
    
    def sector(self):
        if self.screen_dict is not None:
            return self.screen_dict["Sector"]
        return self.attr_dict["Sector"]
      
    def rsi_value(self):
        if self.rsi is None:
            self.rsi = metric.rsi(self.close_prices())
        return self.rsi
    
    def rsi_str(self):
        self.rsi_value()
        if self.rsi >= 65:
            return "<font color=\"red\">Overbought</font>"
        if self.rsi <= 30: 
            return "<font color=\"green\">Oversold</font>"
        return "<font color=\"orange\">Normal</font>"
    
    def ma_diff_value(self):
        if self.ma_diff is None:
            self.ma_diff = metric.ma_diff_ratio(
                                self.close_prices(), 20, 50)
        return self.ma_diff

    def ma_diff_str(self):
        self.rsi_value()
        if self.ma_diff >= -0.005 and self.ma_diff <= 0.01:
            return "<font color=\"green\">Good Buy</font>"
        if self.ma_diff > 0.01:
            return "<font color=\"red\">Overbought</font>"
        return "<font color=\"orange\">Negative</font>"
    
    def perf_rate(self):
        perf_year = misc.to_float_value(self.attr_dict['Perf Year'])
        perf_half_year = misc.to_float_value(self.attr_dict['Perf Half Y'])
        perf_quarter = misc.to_float_value(self.attr_dict['Perf Quarter'])
        perf_month = misc.to_float_value(self.attr_dict['Perf Month'])
       
        weekly_perf = [
                       metric.compound(perf_year/100, 52), 
                       metric.compound(perf_half_year/100, 26),
                       metric.compound(perf_quarter/100, 13),
                       metric.compound(perf_month/100, 4.3),
                       ]
        return metric.slope(weekly_perf)
    
    def perf_rate_str(self):
        perf_rate = self.perf_rate()
        if perf_rate < -0.1:
            return "<font color=\"red\">Slowing down</font>"
        if perf_rate > 0.1: 
            return "<font color=\"green\">Speeding up</font>"
        return "<font color=\"orange\">Consistent</font>"
