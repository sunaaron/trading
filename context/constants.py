#!/usr/bin/python
'''
Created on Nov 10, 2017

@author: Aaron
'''

# finviz_sector_url = "http://finviz.com/groups.ashx?g=sector&v=140&o=name"
finviz_quote_url = "http://finviz.com/quote.ashx?t=%s"
finviz_img_url = "http://finviz.com/chart.ashx?t=%s&ty=c&ta=1&p=d&s=l"
finviz_screen_url = "https://finviz.com/screener.ashx?v=111&f=cap_midover,fa_eps5years_o10,fa_epsyoy_pos,fa_netmargin_o5,fa_pe_profitable,fa_sales5years_o10,geo_usa,sh_relvol_o1.5,ta_change_u1,ta_sma200_pa&ft=4&o=sector"
# 
# yahoo_url = "http://finance.yahoo.com"
yahoo_q_url = "http://finance.yahoo.com/q?s=%s"
yahoo_hp_url =  "https://finance.yahoo.com/quote/%s/history/"

dropbox_watchlist_url = "https://www.dropbox.com/s/v57rb9bvfc5t40h/Watchlist.txt"

# 
# csv_path = 'input/finviz.csv'
# 
# stats_attr_lst = ['Desc', 'Market Cap', 'P/E', 'Forward P/E', 'PEG', 'Sales past 5Y', 'Sales Q/Q', 'EPS this Y',
#                   'EPS past 5Y', 'EPS Q/Q', 'Shs Float', 'Short Float', 'Dividend %', 'Earnings', 'Price']
# metric_attr_lst = ['up_str', 'down_str', 'MA_DIFF_UP_5_13']