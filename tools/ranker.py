'''
Created on Jan 3, 2018

@author: Aaron
'''
from collections import defaultdict

import scipy 

from context import constants
from ioutil import diskman


def extract_symbol_metric_dict(date_symbol_dict, metric_method_name):
    symbol_metric_dict = defaultdict(list)
    for date in date_symbol_dict:
        for symbol_str in date_symbol_dict[date]:
            symbol_obj = date_symbol_dict[date][symbol_str]
            value = symbol_obj.__getattribute__(metric_method_name)()
            symbol_metric_dict[symbol_str].append(value)
    return symbol_metric_dict

def get_ranking_dict(symbol_metric_dict):
    '''
    output is like {'VPU': 44, 'XBI': 1}
    '''
    avg_metric_lst = [
        (scipy.mean(symbol_metric_dict[symbol_str]), 
         symbol_str) for symbol_str in symbol_metric_dict]
    avg_metric_lst.sort(reverse=True)
    ranking_dict = {}
    for i in xrange(len(avg_metric_lst)):
        symbol_str = avg_metric_lst[i][1]
        ranking_dict[symbol_str] = i+1
    return ranking_dict

def process(today_metric_dict, old_metric_dict):
    obsolete_symbols = []
    for symbol in old_metric_dict:
        if symbol not in today_metric_dict:
            obsolete_symbols.append(symbol)
    for symbol in obsolete_symbols:
        del old_metric_dict[symbol]
        
    for symbol in constants.sticky_dict:
        try:
            del today_metric_dict[symbol]
            del old_metric_dict[symbol]
        except KeyError:
            continue

    today_ranking_dict = get_ranking_dict(today_metric_dict)
    old_ranking_dict = get_ranking_dict(old_metric_dict)
    for symbol in today_ranking_dict:
        if symbol in old_ranking_dict:
            today_ranking_dict[symbol] = (today_ranking_dict[symbol], 
                                          old_ranking_dict[symbol] - today_ranking_dict[symbol])
        else:
            today_ranking_dict[symbol] = (today_ranking_dict[symbol], 'N/A')
    return today_ranking_dict

def get_relative_ranking_dict(today_date_symbol_dict,
                              old_date_symbol_dict,
                              metric_method_name):
    '''
    output is like {'VPU': (44, -2), 'XBI': (1, 3)}
    The second element of the value is the relative position change
    '''
    today_metric_dict = extract_symbol_metric_dict(today_date_symbol_dict, 
                                                   metric_method_name)
    old_metric_dict = extract_symbol_metric_dict(old_date_symbol_dict, 
                                                 metric_method_name)
    return process(today_metric_dict, old_metric_dict)
    
def get_relative_ranking_dicts():
    pickle_paths = diskman.get_pickle_path_today()
    today_date_symbol_dict = diskman.load_symbol_dict_by_date(pickle_paths)
    
    pickle_paths = diskman.get_pickle_paths_last_week()
    old_date_symbol_dict = diskman.load_symbol_dict_by_date(pickle_paths)
    
    relative_rank_y2_dict = get_relative_ranking_dict(today_date_symbol_dict, 
                                                      old_date_symbol_dict, 
                                                      "perf_trend_since_half_year")
    relative_rank_y_dict = get_relative_ranking_dict(today_date_symbol_dict, 
                                                     old_date_symbol_dict, 
                                                     "perf_trend_since_year")
    return (relative_rank_y2_dict, relative_rank_y_dict)
