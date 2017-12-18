'''
Created on Nov 11, 2017

@author: Aaron
'''
from module import metric
from tools import misc
from ioutil import html

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
        
    def to_dict(self):
        symbol_dict = {}
        for attr in self.dict_attrs:
            symbol_dict[attr] = self.__getattribute__(attr)
        return symbol_dict
    
    def from_dict(self, symbol_dict):
        for attr in self.dict_attrs:
            self.__setattr__(attr, symbol_dict[attr])
            
    def __setattr__(self, name, value):
        super(Symbol, self).__setattr__(name, value)
        if name == 'history_prices' and value is not None:
            vals = value.close_prices()
            ma_13 = metric.ma(vals, 13)
            ma_20 = metric.ma(vals, 20)
            ma_34 = metric.ma(vals, 34)
            ma_50 = metric.ma(vals, 50)
            
            self.ma_diff_short = metric.MADIFF(
                                    vals, ma_13, ma_34)
            self.ma_diff_medium = metric.MADIFF(
                                    vals, ma_13, ma_50)
            self.ma_diff_long = metric.MADIFF(
                                    vals, ma_20, ma_50)
            # The idea is for long term trend, such as rally-days, 
            # use ma_diff_long
            
            # for short term trend, such as rally-gain, use ma_diff_short
            # for others, either is fine
            self.ma_diff_dict = {
                                 'LONG': self.ma_diff_long,
                                 'MEDIUM': self.ma_diff_medium, 
                                 'SHORT': self.ma_diff_short,
                                 }
            
    def latest_date(self):
        """ datetime.datetime type
        """
        return self.history_prices.daily_summaries[-1].date
    
    def is_newer_than(self, another):
        return self.latest_date() > another.latest_date()

    def open_prices(self):
        return self.history_prices.open_prices()
        
    def close_prices(self):
        return self.history_prices.close_prices()
    
    def change(self):
        return float(self.attr_dict["Change"][:-1])
    
    def change_html(self):
        change = self.change()
        change_str = str(change) + '%'
        if change >= 1:
            return html.green(change_str)
        if change < 0:
            return html.red(change_str)
        return html.orange(change_str)
    
    def relative_volume(self):
        return float(self.attr_dict["Rel Volume"])

    def is_high_volume(self):
        return self.relative_volume() >= 1.5
    
    def relative_volume_html(self):
        rel_vol = self.relative_volume()
        if rel_vol > 1.2:
            return html.green(rel_vol)
        if rel_vol <= 1.2 and rel_vol >= 0.8:
            return html.orange(rel_vol)
        return html.red(rel_vol)
    
    def sector(self):
        if self.screen_dict is not None:
            return self.screen_dict["Sector"]
        return self.attr_dict["Sector"]
      
    def rsi_value(self):
        return misc.to_float_value(self.attr_dict['RSI (14)'])
    
    def rsi_html(self):
        rsi = self.rsi_value()
        if rsi >= 65:
            return html.red(rsi)
        if rsi <= 30:
            return html.green(rsi)
        return html.orange(rsi)
    
    def ma_diff_ratio(self, tp='LONG'):
        ma_obj = self.ma_diff_dict[tp]
        return ma_obj.ratio()
    
    def ma_diff_ratio_html(self):
        return str(self.ma_diff_ratio())
    
    def ma_diff_trend(self, tp='LONG'):
        ma_obj = self.ma_diff_dict[tp]
        return ma_obj.trend()
        
    def ma_diff_trend_html(self):
        if self.ma_diff_trend() >= 0:
            return html.green('&#8679;')
        return html.orange('&#8681;')

    def ma_rally_days(self, tp='LONG'):
        ma_obj = self.ma_diff_dict[tp]
        return ma_obj.rally_days()

    def ma_rally_days_html(self):
        days = self.ma_rally_days()
        if days >= 20:
            return html.red(days)
        if days <= 5:
            return html.orange(days)
        return html.green(days)
    
    def ma_rally_gain(self):
        return max((self.ma_diff_short.rally_gain(), 
                    self.ma_diff_medium.rally_gain()))

    def ma_rally_gain_html(self):
        gain = self.ma_rally_gain() * 100
        gain_str = str(gain) + '%'
        if gain <= 3:
            return html.green(gain_str)
        if gain > 3 and gain < 7:
            return html.orange(gain_str)
        return html.red(gain_str)

    def perf_weekly_by_year(self):
        perf_year_str = self.attr_dict['Perf Year'] == '-' and \
            self.attr_dict['Perf YTD'] or self.attr_dict['Perf Year']
        perf_year = misc.to_float_value(perf_year_str)
        return metric.compound(perf_year/100, 52)
    
    def perf_weekly_by_half_year(self):
        perf_half_year = misc.to_float_value(self.attr_dict['Perf Half Y'])
        return metric.compound(perf_half_year/100, 26)
        
    def perf_weekly_by_quarter(self):
        perf_quarter = misc.to_float_value(self.attr_dict['Perf Quarter'])
        return metric.compound(perf_quarter/100, 13)
        
    def perf_weekly_by_month(self):
        perf_month = misc.to_float_value(self.attr_dict['Perf Month'])
        return metric.compound(perf_month/100, 4.33)

    def perf_weekly_by_14_day(self):
        num_days = 14
        if len(self.close_prices()) < num_days:
            return -1
        perf = (self.close_prices()[-1] - 
                self.close_prices()[-num_days]) / self.close_prices()[-num_days]
        return metric.compound(perf, num_days/5.0) # 14 business days = 2.8 wks
    
    def perf_trend_since_half_year(self):
        return metric.slope([
                             self.perf_weekly_by_half_year(),
                             self.perf_weekly_by_quarter(),
                             self.perf_weekly_by_month(),
                             self.perf_weekly_by_14_day()
                             ])
    
    def perf_trend_since_year(self):
        return metric.slope([
                             self.perf_weekly_by_year(),
                             self.perf_weekly_by_half_year(),
                             self.perf_weekly_by_quarter(),
                             self.perf_weekly_by_month(),
                             ])
    
    def perf_trend_html(self, perf_rate):
        if perf_rate < -0.02:
            return html.red(perf_rate)
        if perf_rate > 0.1:
            return html.green(perf_rate)
        return html.orange(perf_rate)
    
    def yearly_perf_html(self, value_str):
        if value_str == 'N/A':
            return value_str
        value = misc.to_float_value(value_str)
        if value >= 10:
            return html.green(value_str)
        if value >= 3:
            return html.orange(value_str)
        return html.red(value_str)

    def beta_html(self, value_str):
        if value_str == 'N/A':
            return value_str
        value = misc.to_float_value(value_str)
        if value >= 1.25:
            return html.red(value_str)
        if value >= 1.05:
            return html.orange(value_str)
        return html.green(value_str)
