'''
Created on Dec 9, 2017

@author: Aaron
'''
from context import constants


def red(text):
    return "<font color=\"red\">%s</font>" % text

def green(text):
    return "<font color=\"green\">%s</font>" % text

def orange(text):
    return "<font color=\"orange\">%s</font>" % text

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
    
def fund_watch_html_str(symbol_obj):
    yahoo_url = constants.yahoo_q_url % symbol_obj.symbol
    html_str = '<tr><td align=\"left\" valign=\"top\" width=\"33%\">'
    html_str = '%s<a href=\"%s\">%s</a>' % (html_str, 
                                            yahoo_url, 
                                            symbol_obj.symbol)
    
    html_str = "%s<br>%s" %(html_str, symbol_obj.desc)

    html_str = "%s<br>%s: %s" %(html_str, 
                                "<b>Expense Ratio</b>", 
                                symbol_obj.expense_ratio())
    
    html_str = "%s<br>%s: %s (%s)" %(html_str, 
                                     "<b>P/E</b>", 
                                     symbol_obj.fund_pe(), 
                                     symbol_obj.fund_pe_str())
    
    html_str = "%s<br>%s: %s (%s)" %(html_str, 
                                     "<b>Rsi</b>", 
                                     symbol_obj.rsi_value(), 
                                     symbol_obj.rsi_str())
    
    html_str = "%s<br>%s: %s (%s)" %(html_str, 
                                     "<b>Ma_diff</b>", 
                                     symbol_obj.ma_diff_value(), 
                                     symbol_obj.ma_diff_str())
    
    html_str = "%s<br>%s: %s <b>/</b> %s" %(html_str, 
                                     "<b>Perf Year / Half Y</b>",
                                     symbol_obj.attr_dict['Perf Year'], 
                                     symbol_obj.attr_dict['Perf Half Y'])

    html_str = "%s<br>%s: %s <b>/</b> %s" %(html_str, 
                                     "<b>Perf Quarter / Month</b>",
                                     symbol_obj.attr_dict['Perf Quarter'], 
                                     symbol_obj.attr_dict['Perf Month'])
    
    html_str = "%s<br>%s: %s (%s)" %(html_str, 
                                     "<b>Perf rate</b>",
                                     symbol_obj.perf_rate(), 
                                     symbol_obj.perf_rate_str())
    
    html_str = "%s<br>%s: %s (%s)" %(html_str, 
                                     "<b>Relative vol</b>", 
                                     symbol_obj.relative_volume(), 
                                     symbol_obj.relative_volume_str())

    html_str = "%s<br>%s: %s" %(html_str, 
                                "<b>Dividend</b>", 
                                symbol_obj.attr_dict['Dividend %'])
    
    html_str += gen_finviz_image_td(symbol_obj.symbol)
    html_str += gen_holdings_td(symbol_obj.holdings())
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
