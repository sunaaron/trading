'''
Created on Dec 9, 2017

@author: Aaron
'''
from model.symbol import Symbol
from module import metric
from tools import misc

class StockSymbol(Symbol):
    dict_attrs = [
                  "symbol", "symbol_type",
                  "screen_dict", "attr_dict", 
                  "rsi", "ma_diff",  
                  "annual_sales", "annual_incomes", 
                  "quarterly_sales", "quarterly_incomes",
                  ]

    def __init__(self, symbol):
        super(StockSymbol, self).__init__(symbol)
        self.symbol_type = "stock"
        self.screen_dict = None

        self.annual_sales = None
        self.quarterly_sales = None
        self.annual_incomes = None
        self.quarterly_incomes = None
        
    def __gen_growth(self, value_lst, as_percent=True):
        growth = []
        values = [misc.to_float_value(v) 
                  for v in value_lst]
        for i in xrange(1, len(values)):
            change = (values[i] - values[i-1])/values[i-1]
            if as_percent:
                growth.append(misc.to_percent(change))
            else:
                growth.append(change)
        return growth

    def sales(self):
        return self.attr_dict['Sales']
    
    def income(self):
        return self.attr_dict['Income']

    def num_of_employee(self):
        return int(self.attr_dict['Employees'])
    
    def sales_per_employee(self):
        if self.sales() == '-':
            return ''
        sales = misc.to_float_value(self.sales())
        return sales / self.num_of_employee()
        
    def sales_per_employee_str(self):
        return misc.to_M_value(self.sales_per_employee()) 

    def income_per_employee(self):
        if self.income() == '-':
            return ''
        income = misc.to_float_value(self.income())
        return income/self.num_of_employee()
    
    def income_per_employee_str(self):
        return misc.to_M_value(self.income_per_employee())
    
    def num_shares(self):
        return misc.to_float_value(self.attr_dict['Shs Outstand'])
        
    def cash(self):
        if self.attr_dict['Cash/sh'] == "-":
            return 0
        cash_per_share = misc.to_float_value(
                            self.attr_dict['Cash/sh'])
        return self.num_shares() * cash_per_share
    
    def cash_str(self):
        return misc.to_B_value(self.cash())
    
    def cash_per_employee(self):
        return self.cash()/self.num_of_employee()
    
    def cash_per_employee_str(self):
        return misc.to_M_value(self.cash_per_employee())
        
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
