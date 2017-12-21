'''
Created on Dec 9, 2017

@author: Aaron
'''
from context import constants
from tools import filter

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

def gen_finviz_image_td(symbol_str, img_url):
    img_src = img_url % symbol_str
    html_str = '<td align=\"left\" valign=\"top\" width=\"50%\">'
    html_str = '%s<img src=\"%s\"' %(html_str, img_src)
    html_str += ' style=\"width:400px; height:auto;\"/></td>'
    return html_str  

def gen_perf_td(symbol_obj):
    html_str = '<td align=\"left\" valign=\"top\">'
    for tp in ('1-Year', '3-Year', '5-Year', '10-Year',
                 '2017', '2016', '2015',
                 '2014', '2013', '2012'):
        perf_str = symbol_obj.fund_perf(tp)
        html_str += '<span style=\"width:25px;\">%s</span>: ' \
                    % tp
        
        html_str += symbol_obj.yearly_perf_html(perf_str)
        html_str += '<br>'
        if tp == '10-Year':
            html_str += '<br>'
    
    html_str += '</td>'
    return html_str

def gen_left_td(symbol_obj):
    finviz_url = constants.finviz_quote_url % symbol_obj.symbol
    html_str = '<tr><td align=\"left\" valign=\"top\" width=\"28%\">'
    html_str = '%s<strong><a href=\"%s\">%s</a></strong>' % (
                    html_str, finviz_url, symbol_obj.symbol)
    
    if symbol_obj.is_pick_today():
        html_str = "%s (&#9733; %s &#9733;)" % (html_str, green("PoD"))
        
    if symbol_obj.is_high_volume():
        html_str = "%s (&#9889; %s &#9889;)" % (html_str, orange("HV"))

    yahoo_url = constants.yahoo_holdings_url % symbol_obj.symbol    
    html_str = "%s<br><a href=\"%s\">%s</a>" %(
                    html_str, yahoo_url, symbol_obj.desc)

    html_str = "%s<br>%s: %s" %(html_str, 
                                "Change", 
                                symbol_obj.change_html())
    
    html_str = "%s<br>%s: %s" %(html_str, 
                                "RSI", 
                                symbol_obj.rsi_html())

    if symbol_obj.ma_rally_days() > 0:
        html_str = "%s<br>%s(%s): %s for %s days" %(
                        html_str,
                        "Ma_gain",
                        symbol_obj.ma_diff_trend_html(),
                        symbol_obj.ma_rally_gain_html(),
                        symbol_obj.ma_rally_days_html())
    else:
        html_str = "%s<br>%s(%s): %s" %(html_str, "Ma_diff",  
                                        symbol_obj.ma_diff_trend_html(),
                                        symbol_obj.ma_diff_ratio_html())

    html_str = "%s<br>%s: %s / %s" %(html_str, 
            "Perf Momentum",
            symbol_obj.perf_trend_html(symbol_obj.perf_trend_since_year()),
            symbol_obj.perf_trend_html(symbol_obj.perf_trend_since_half_year()) 
            )
    
    html_str = "%s<br><u style=\"text-decoration-color: darkgray;\">%s: %s%s</u>" %(
                html_str, 
                "Relative vol", 
                symbol_obj.relative_volume_html(), 
                "&nbsp;"*24)
    
    html_str = "%s<br>%s: %s" %(html_str, 
                                "P/E", 
                                symbol_obj.fund_pe_html())

    beta = symbol_obj.five_year_beta()
    html_str = "%s<br>%s: %s" %(html_str, 
                                "5YR-Beta", 
                                symbol_obj.beta_html(beta))
    
    treynor = symbol_obj.five_year_treynor()
    html_str = "%s<br>%s: %s" %(html_str, 
                                "5YR-Treynor", 
                                symbol_obj.treynor_html(treynor))
    
    html_str = "%s<br>%s: <b>%s</b>" %(html_str, 
                                       "Dividend", 
                                       symbol_obj.attr_dict['Dividend %'])
    
    html_str = "%s<br>%s: %s" %(html_str, 
                                "Expense Ratio", 
                                symbol_obj.expense_ratio_html())
    html_str += "</td>"
    return html_str
    
def fund_watch_html_str(symbol_obj):
    html_str = gen_left_td(symbol_obj)
    html_str += gen_finviz_image_td(symbol_obj.symbol, 
                                    constants.finviz_weekly_img_url)
    html_str += gen_perf_td(symbol_obj)
    html_str += '</tr>'
    return html_str

def get_index_symbols(symbol_lst):
    return [s for s in symbol_lst \
                if s.symbol in constants.mkt_index]

def get_non_index_symbols(symbol_lst):
    return [s for s in symbol_lst \
                if not s.symbol in constants.mkt_index]

def gen_watchlist_fund_html(symbol_lst):
    # Sort first by perf_trend_since_year and relative_volume
    symbol_lst = filter.filter_tenure_less_than_a_year(symbol_lst)
    symbol_tuple_lst = [((symbol_obj.is_pick_today(), 
                          symbol_obj.perf_trend_since_half_year()), 
                         symbol_obj) for symbol_obj in symbol_lst]
    symbol_tuple_lst.sort(reverse=True)
    sorted_symbol_lst = [tp[1] for tp in symbol_tuple_lst]
    
    final_symbol_lst = get_index_symbols(sorted_symbol_lst)
    final_symbol_lst.extend(get_non_index_symbols(sorted_symbol_lst))

    html_str = gen_table_header()
    
    for symbol_obj in final_symbol_lst:
        html_str += fund_watch_html_str(symbol_obj)
        html_str += '<tr></tr>'
    
    html_str += gen_table_footer()
    return html_str
