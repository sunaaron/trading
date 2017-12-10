'''
Created on Dec 9, 2017

@author: Aaron
'''
from context import constants


def red(text):
    return "<strong style=\"color: red;\">%s</strong>" % text

def green(text):
    return "<strong style=\"color: green;\">%s</strong>" % text

def orange(text):
    return "<strong style=\"color: orange;\">%s</strong>" % text

def gen_table_header():
    return '<html><head><body><table>'

def gen_table_footer():
    return '</table></body></head></html>'

def gen_finviz_image_td(symbol_str):
    img_src = constants.finviz_img_url % symbol_str
    html_str = '<td align=\"left\" valign=\"top\" width=\"50%\">'
    html_str = '%s<img src=\"%s\"' %(html_str, img_src)
    html_str += ' style=\"width:400px; height:auto;\"/></td>'
    return html_str  

def gen_holdings_td(holdings):
    if len(holdings) == 0:
        return ''
    html_str = '<td align=\"left\" valign=\"top\">'
    for holding in holdings:
        html_str += '<span style=\"width:25px;\">%s</span>: ' % holding[1]
        html_str += '<span>%s</span>' % holding[2]
        html_str += '<br>'
    html_str += '</td>'
    return html_str

def gen_perf_td(symbol_obj):
    perf_dict = symbol_obj.fund_perf_dict
    html_str = '<td align=\"left\" valign=\"top\">'
    for perf in perf_dict['yearly'][:6]:
        html_str += '<span style=\"width:25px;\">%s</span>: ' \
                    % perf[0]
        html_str += symbol_obj.yearly_return_str(perf[1])
        html_str += '<br>'
    
    yrt_3 = perf_dict['3-year']
    html_str = "%s%s: %s" %(html_str, 
                            "3-YR",
                            symbol_obj.yearly_return_str(yrt_3)) 
    yrt_5 = perf_dict['5-year']
    html_str = "%s<br>%s: %s" %(html_str, 
                                "5-YR", 
                                symbol_obj.yearly_return_str(yrt_5))
    
    html_str += '</td>'
    return html_str
    
def fund_watch_html_str(symbol_obj):
    yahoo_url = constants.yahoo_holdings_url % symbol_obj.symbol
    html_str = '<tr><td align=\"left\" valign=\"top\" width=\"27%\">'
    html_str = '%s<a href=\"%s\">%s</a>' % (html_str, 
                                            yahoo_url, 
                                            symbol_obj.symbol)
    
    html_str = "%s<br>%s" %(html_str, symbol_obj.desc)

    html_str = "%s<br>%s: %s" %(html_str, 
                                "Rsi", 
                                symbol_obj.rsi_str())
    
    html_str = "%s<br>%s: %s" %(html_str, 
                                "Ma_diff", 
                                symbol_obj.ma_diff_str())

    perf_year = symbol_obj.attr_dict['Perf Year']
    html_str = "%s<br>%s: %s" %(html_str, 
                                "Perf Year",
                                symbol_obj.yearly_return_str(perf_year))
    
    html_str = "%s<br>%s: %s" %(html_str, 
                                "Perf Momentum",
                                symbol_obj.perf_rate_str())
    
    html_str = "%s<br>%s: %s" %(html_str, 
                                "Relative vol", 
                                symbol_obj.relative_volume_str())

    html_str = "%s<br>%s: <b>%s</b>" %(html_str, 
                                       "Dividend", 
                                       symbol_obj.attr_dict['Dividend %'])
    
    html_str = "%s<br>%s: %s" %(html_str, 
                                "Expense Ratio", 
                                symbol_obj.expense_ratio_str())
    
    html_str = "%s<br>%s: %s" %(html_str, 
                                "P/E", 
                                symbol_obj.fund_pe_str())

    html_str += gen_finviz_image_td(symbol_obj.symbol)
    html_str += gen_perf_td(symbol_obj)
    html_str += '</tr>'
    return html_str

def gen_watchlist_fund_html(symbol_lst):
    # Sort first by perf_rate and relative_volume
    symbol_tuple_lst = [((symbol_obj.perf_rate(), symbol_obj.relative_volume()), 
                         symbol_obj) for symbol_obj in symbol_lst]
    symbol_tuple_lst.sort(reverse=True)
    sorted_symbol_lst = [tp[1] for tp in symbol_tuple_lst]
    
    html_str = gen_table_header()
    
    for symbol_obj in sorted_symbol_lst:
        html_str += fund_watch_html_str(symbol_obj)
    
    html_str += gen_table_footer()
    return html_str
