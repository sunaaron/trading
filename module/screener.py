'''
Created on Nov 24, 2017

@author: Aaron
'''
from context import constants
from ioutil import diskman
from tools import fetcher, parser, hydrator

def fetch_all_symbols():
    """
    Fetch all symbols from the Finviz screen page and store them to screen.txt
    """
    screen_data = fetcher.fetch_screen_list_from_finviz(
                    constants.finviz_screen_url)
    a_lst = parser.parse_screen_list_urls_from_finviz(screen_data)
    a_lst.insert(0, constants.finviz_screen_url)
         
    symbol_lst = []
    for a in a_lst:
        screen_data = fetcher.fetch_screen_list_from_finviz(a)
        symbol_lst.extend(parser.parse_screen_list_from_finviz(screen_data))
     
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
    
    batch_symbols = []
    for i in xrange(len(diff_symbols)):
        batch_symbols.append(diff_symbols[i])
        if (i+1)%10 == 0 or i == len(diff_symbols)-1:
            print i
            hydrator.hydrate_complete(batch_symbols)
            diskman.dump_symbol_dict_by_pickle(batch_symbols)
            batch_symbols = []

def gen_caption():
    caption_str = ""
    caption_str += "Symbol" + "\t"
    caption_str += "Sector" + "\t"
    caption_str += "Industry" + "\t"
    caption_str += "P/E" + "\t"
    caption_str += "Sales Per Employee" + "\t"
    caption_str += "Sales Per Employee (M)" + "\t"
    caption_str += "Profit Per Employee" + "\t"
    caption_str += "Profit Per Employee (M)" + "\t"
    caption_str += "Cash Per Employee" + "\t"
    caption_str += "Cash Per Employee(M)" + "\t"
    caption_str += "Dividend %" + "\t"
    caption_str += "Perf YTD" + "\t"
    caption_str += "Beta" + "\t"
    caption_str += "Sales past 5Y" + "\t"
    caption_str += "Annual Sales Growth" + "\t"
    caption_str += "EPS past 5Y" + "\t"
    caption_str += "Annual Income Growth" + "\t"
    caption_str += "Sales Q/Q" + "\t"
    caption_str += "Quarterly Sales Growth" + "\t"
    caption_str += "EPS Q/Q" + "\t"
    caption_str += "Quarterly Income Growth" + "\t"
    return caption_str.rstrip("\t")

def gen_row(symbol_obj):
    row_str = ""
    row_str += symbol_obj.symbol + "\t"
    row_str += symbol_obj.attr_dict["Sector"] + "\t"
    row_str += symbol_obj.attr_dict["Industry"] + "\t"
    row_str += symbol_obj.attr_dict["P/E"] + "\t"
    row_str += str(symbol_obj.sales_per_employee()) + "\t"
    row_str += symbol_obj.sales_per_employee_str() + "\t"
    row_str += str(symbol_obj.income_per_employee()) + "\t"
    row_str += symbol_obj.income_per_employee_str() + "\t"
    row_str += str(symbol_obj.cash_per_employee()) + "\t"
    row_str += symbol_obj.cash_per_employee_str() + "\t"
    row_str += symbol_obj.attr_dict["Dividend %"] + "\t"
    row_str += symbol_obj.attr_dict["Perf YTD"] + "\t"
    row_str += symbol_obj.attr_dict["Beta"] + "\t"
    row_str += symbol_obj.attr_dict["Sales past 5Y"] + "\t"
    row_str += str(symbol_obj.annual_sales_growth()) + "\t"
    row_str += symbol_obj.attr_dict["EPS past 5Y"] + "\t"
    row_str += str(symbol_obj.annual_income_growth()) + "\t"
    row_str += symbol_obj.attr_dict["Sales Q/Q"] + "\t"
    row_str += str(symbol_obj.quarterly_sales_growth()) + "\t"
    row_str += symbol_obj.attr_dict["EPS Q/Q"] + "\t"
    row_str += str(symbol_obj.quarterly_income_growth()) + "\t"
    
    return row_str.rstrip("\t")
    
def gen_table():
    """
    Process persisted hydration. This is done offline
    """
    symbol_lst = diskman.load_symbols_by_pickle()
    table_str = gen_caption() + "\n"
    for symbol_obj in symbol_lst:
        table_str += gen_row(symbol_obj) + "\n"
    diskman.save_screen_table(table_str)

def screen_manually():
    fetch_all_symbols()
    update_union_and_diff()
    hydrate_and_dump_diff_symbols()
    gen_table()