'''
Created on Nov 11, 2017

@author: Aaron
'''
from tools import misc
import numpy

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
    
    def get_close_prices(self):
        return [ds.close for ds in self.daily_summaries] 
    
    def get_open_prices(self):
        return [ds.open for ds in self.daily_summaries]

class Symbol(object):
    
    def __init__(self, symbol, attr_dict):
        self.symbol = symbol
        self.attr_dict = attr_dict
        
    def __convert_float_value(self, value_str):
        value = float(value_str[:-1])
        unit = value_str[-1]
        return value * misc.get_multiplier(unit)
    
    def __convert_M_value(self, num):
        num = num / 1000000
        return "%sM" % str(round(num, 2)) 
        
    def get_sales(self):
        return self.attr_dict['Sales']
    
    def get_income(self):
        return self.attr_dict['Income']

    def get_num_of_employee(self):
        return int(self.attr_dict['Employees'])
    
    def get_sales_per_employee(self):
        sales = self.__convert_float_value(self.get_sales())
        sales_per_employee = sales / self.get_num_of_employee()
        return self.__convert_M_value(sales_per_employee) 

    def get_income_per_employee(self):
        income = self.__convert_float_value(self.get_income())
        income_per_employee = income/self.get_num_of_employee()
        return self.__convert_M_value(income_per_employee)
