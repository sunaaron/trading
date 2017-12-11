'''
Created on Nov 28, 2017

@author: Aaron
'''
from module.screener import *
from ioutil import csv

if __name__ == '__main__':
    fetch_all_symbols()
    update_union_and_diff()
    hydrate_and_dump_diff_symbols()
    csv.gen_stock_table()
#     csv.gen_fund_table()
    