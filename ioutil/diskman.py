'''
Created on Nov 19, 2017

@author: Aaron
'''
import os
import pickle

from tools import dateutil
from model.stock_symbol import StockSymbol
from model import helper

def get_year_month_path():
    year_month_str = dateutil.get_year_month()
    year_month_path = "./data/%s" % year_month_str
    if not os.path.exists(year_month_path):
        os.mkdir(year_month_path)
    return year_month_path

def save_symbol_as_str(symbol_lst, path):
    output_str = ""
    for symbol in symbol_lst:
        output_str += symbol.symbol + "\n"
    with open(path, "w") as f:
        f.write(output_str.rstrip("\n"))
    f.close()
    
def save_symbol_set_as_str(symbol_set, path):
    output_lst = []
    for symbol in symbol_set:
        output_lst.append(symbol)
    output_lst.sort()
    output_str = "\n".join(output_lst)
    with open(path, "w") as f:
        f.write(output_str.rstrip("\n"))
    f.close()
    
def load_symbol_as_object(path):
    symbol_file = open(path, "r")
    symbol_strs = symbol_file.read().split("\n")
    return [StockSymbol(symbol_str.rstrip('\r')) for symbol_str in symbol_strs]

def load_symbol_as_str(path):
    symbol_file = open(path, "r")
    symbol_strs = symbol_file.read().split("\n")
    return [symbol_str.rstrip('\r') for symbol_str in symbol_strs]

def dump_symbol_lst_by_pickle(symbol_lst):
    symbol_strs = []
    symbol_dict = {}
    for symbol_obj in symbol_lst:
        symbol_str = symbol_obj.symbol
        symbol_strs.append(symbol_obj.symbol)
        symbol_dict[symbol_str] = symbol_obj.to_dict()
    symbol_strs.sort()
    path = "./data/%s_%s_%s.pickle" % (symbol_strs[0], 
                                       symbol_strs[-1], 
                                       str(dateutil.get_today_date()))
    with open(path, "w") as f:
        pickle.dump(symbol_dict, f) 
    f.close()

def load_symbol_dict_by_pickle():
    symbol_dict = {}
    path_lst = os.listdir("./data")
    pickle_paths = ["./data/%s" % p 
                    for p in path_lst if p.endswith(".pickle")]
    if len(pickle_paths) == 0:
        return symbol_dict
    
    for path in pickle_paths:
        with open(path, "r") as f:
            pickle_dict = pickle.load(f)
            for symbol_str in pickle_dict:
                symbol_type = pickle_dict[symbol_str]['symbol_type']
                symbol_obj = helper.gen_symbol_obj(
                                symbol_str, symbol_type)
                symbol_obj.from_dict(pickle_dict[symbol_str])
                if not symbol_str in symbol_dict:
                    symbol_dict[symbol_str] = symbol_obj
                else:
                    if symbol_obj.is_newer_than(symbol_dict[symbol_str]):
                        symbol_dict[symbol_str] = symbol_obj
    
    return symbol_dict

def load_symbol_lst_by_pickle():
    symbol_dict = load_symbol_dict_by_pickle()
    return symbol_dict.values()
    
def save_csv(csv_str):
    with open("./data/csv.txt", "w") as f:
        f.write(csv_str)
    f.close()
