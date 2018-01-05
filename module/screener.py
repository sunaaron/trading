'''
Created on Nov 24, 2017

@author: Aaron
'''
from context import constants
from ioutil import diskman
from tools import (
                   fetcher, 
                   filter, 
                   hydrator, 
                   parser,
                   )

def fetch_all_symbols():
    """
    Fetch all symbols from the Finviz screen page and store them to screen.txt
    Sector = Financial will not be included
    """
    screen_data = fetcher.fetch_screen_list_from_finviz(
                    constants.finviz_screen_url)
    a_lst = parser.parse_screen_list_urls_from_finviz(screen_data)
    a_lst.insert(0, constants.finviz_screen_url)
         
    symbol_lst = []
    for a in a_lst:
        screen_data = fetcher.fetch_screen_list_from_finviz(a)
        symbol_lst.extend(parser.parse_screen_list_from_finviz(screen_data))
    symbol_lst = filter.filter_financial_sector(symbol_lst)
    diskman.save_symbol_as_str(symbol_lst, "./data/screen.txt")

def update_union_and_diff():
    """
    Compare the previous combined screen results
    and update the union and diff
    """
    existing_symbols = set(diskman.load_symbol_as_str("./data/existing.txt"))
    screen_symbols = set(diskman.load_symbol_as_str("./data/screen.txt"))
    
    diff_symbols = screen_symbols.difference(existing_symbols)
    union_symbols = screen_symbols.union(existing_symbols)
    
    diskman.save_symbol_set_as_str(diff_symbols, "./data/diff.txt")
    diskman.save_symbol_set_as_str(union_symbols, "./data/union.txt")

def hydrate_and_dump_diff_symbols():
    """
    For all diff symbols, do complete hydration, and persist by pickle
    """
    diff_symbols = diskman.load_symbol_as_object("./data/diff.txt")
    hydrator.batch_hydrate(diff_symbols, hydrator.hydrate_complete)
    diskman.dump_symbol_lst(diff_symbols)
