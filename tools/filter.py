'''
Created on Nov 28, 2017

@author: Aaron
'''
def filter_financial_sector(symbol_lst):
    filtered_symbol_lst = [symbol_obj for symbol_obj in symbol_lst 
                           if symbol_obj.sector() != 'Financial']
    return filtered_symbol_lst

def filter_insignificant_change(symbol_lst):
    filtered_symbol_lst = []
    for symbol_obj in symbol_lst:
        change = symbol_obj.change()
        if change >= 1.0 or change <= -1.0:
            filtered_symbol_lst.append(symbol_obj)
    return filtered_symbol_lst

def filter_weak_volume(symbol_lst):
    filtered_symbol_lst = []
    for symbol_obj in symbol_lst:
        rel_vol = symbol_obj.relative_volume()
        if rel_vol >= 1:
            filtered_symbol_lst.append(symbol_obj)
    return filtered_symbol_lst
