'''
Created on Dec 10, 2017

@author: Aaron
'''
from ioutil import diskman


def gen_stock_caption():
    caption_str = ""
    caption_str += "Symbol" + "\t"
    caption_str += "Sector" + "\t"
    caption_str += "Industry" + "\t"
    caption_str += "Sales Per Employee (M)" + "\t"
    caption_str += "Profit Per Employee (M)" + "\t"
    caption_str += "Profit Margin" + "\t"
    caption_str += "Cash (B)" + "\t"
    caption_str += "Dividend %" + "\t"
    caption_str += "P/E" + "\t"
    caption_str += "Forward P/E" + "\t"
    caption_str += "Perf Year" + "\t"
    caption_str += "Sales past 5Y" + "\t"
    caption_str += "Annual Sales Growth" + "\t"
    caption_str += "Annual Sales Growth Trend" + "\t"
    caption_str += "EPS past 5Y" + "\t"
    caption_str += "Annual Income Growth" + "\t"
    caption_str += "Annual Income Growth Trend" + "\t"
    return caption_str.rstrip("\t")

def gen_stock_row(symbol_obj):
    row_str = ""
    row_str += symbol_obj.symbol + "\t"
    row_str += symbol_obj.attr_dict["Sector"] + "\t"
    row_str += symbol_obj.attr_dict["Industry"] + "\t"
    row_str += symbol_obj.sales_per_employee_str() + "\t"
    row_str += symbol_obj.income_per_employee_str() + "\t"
    row_str += symbol_obj.attr_dict["Profit Margin"] + "\t"
    row_str += symbol_obj.cash_str() + "\t"
    row_str += symbol_obj.attr_dict["Dividend %"] + "\t"
    row_str += symbol_obj.attr_dict["P/E"] + "\t"
    row_str += symbol_obj.attr_dict["Forward P/E"] + "\t"
    row_str += symbol_obj.attr_dict["Perf Year"] + "\t"
    row_str += symbol_obj.attr_dict["Sales past 5Y"] + "\t"
    row_str += str(symbol_obj.annual_sales_growth()) + "\t"
    row_str += str(symbol_obj.annual_sales_growth_trend()) + "\t"
    row_str += symbol_obj.attr_dict["EPS past 5Y"] + "\t"
    row_str += str(symbol_obj.annual_income_growth()) + "\t"
    row_str += str(symbol_obj.annual_income_growth_trend()) + "\t"
    
    return row_str.rstrip("\t")

def gen_stock_table():
    symbol_lst = diskman.load_symbol_lst_by_pickle()
    diskman.dump_symbol_lst_by_pickle(symbol_lst)
    table_str = gen_stock_caption() + "\n"
    for symbol_obj in symbol_lst:
        table_str += gen_stock_row(symbol_obj) + "\n"
    diskman.save_csv(table_str)

def gen_fund_caption():
    caption_str = ""
    caption_str += "Symbol" + "\t"
    caption_str += "Desc" + "\t"
    caption_str += "RSI" + "\t"
    caption_str += "MA_Diff" + "\t"
    caption_str += "Rel Volume" + "\t"
    caption_str += "Perf Momentum" + "\t"
    
    caption_str += "Dividend %" + "\t"
    caption_str += "Exp Ratio" + "\t"
    caption_str += "P/E" + "\t"
    caption_str += "1YR Perf" + "\t"
    caption_str += "3YR Perf" + "\t"
    caption_str += "5YR Perf" + "\t"
    caption_str += "5YR-Beta" + "\t"
    caption_str += "5YR-Treynor" + "\t"

    return caption_str.rstrip("\t")

def gen_fund_row(symbol_obj):
    row_str = ""
    row_str += symbol_obj.symbol + "\t"
    row_str += symbol_obj.desc.rstrip('\r\n') + "\t"
    row_str += str(symbol_obj.rsi) + "\t"
    row_str += str(symbol_obj.ma_diff) + "\t"
    row_str += str(symbol_obj.relative_volume()) + "\t"
    row_str += str(symbol_obj.perf_rate()) + "\t"

    row_str += symbol_obj.attr_dict["Dividend %"] + "\t"
    row_str += symbol_obj.expense_ratio() + "\t"
    row_str += str(symbol_obj.fund_pe()) + "\t"
    row_str += symbol_obj.fund_perf('1-Year') + "\t"
    row_str += symbol_obj.fund_perf('3-Year') + "\t"
    row_str += symbol_obj.fund_perf('5-Year') + "\t"
    row_str += symbol_obj.five_year_beta() + "\t"
    row_str += symbol_obj.five_year_treynor() + "\t"
    
    return row_str.rstrip("\t")

def gen_fund_table():
    symbol_lst = diskman.load_symbol_lst_by_pickle()
    table_str = gen_fund_caption() + "\n"
    for symbol_obj in symbol_lst:
        table_str += gen_fund_row(symbol_obj) + "\n"
    diskman.save_csv(table_str)
