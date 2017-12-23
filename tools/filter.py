'''
Created on Nov 28, 2017

@author: Aaron
'''
import datetime

from tools import dateutil


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

def filter_tenure_less_than_a_year(symbol_lst):
    filtered_symbol_lst = []
    for symbol_obj in symbol_lst:
        if symbol_obj.attr_dict['Perf Half Y'] == '-' or \
                symbol_obj.attr_dict['Perf Quarter'] == '-':
            continue
        else:
            filtered_symbol_lst.append(symbol_obj)
    return filtered_symbol_lst

def filter_local_existent(local_symbol_dict, symbol_lst):
    filtered_symbol_lst = []
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        if not symbol_str in local_symbol_dict:
            filtered_symbol_lst.append(symbol_obj)
                 
    return filtered_symbol_lst

def filter_local_existent_newer_than(local_symbol_dict, symbol_lst, days=0):
    time_now = datetime.datetime.now()
    filtered_symbol_lst = filter_local_existent(local_symbol_dict, symbol_lst)
    
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        if symbol_str in local_symbol_dict:
            symbol_date = local_symbol_dict[symbol_str].latest_date()
            if dateutil.get_diff_days(time_now,symbol_date) > days:
                filtered_symbol_lst.append(symbol_obj)
    return filtered_symbol_lst
