#!/usr/bin/python
'''
Created on Nov 10, 2017

@author: Aaron
'''

# finviz_sector_url = "http://finviz.com/groups.ashx?g=sector&v=140&o=name"
finviz_quote_url = "http://finviz.com/quote.ashx?t=%s"
finviz_weekly_img_url = "http://finviz.com/chart.ashx?t=%s&ty=l&ta=0&p=w&s=l"
finviz_daily_img_url = "http://finviz.com/chart.ashx?t=%s&ty=c&ta=1&p=d&s=l"
finviz_screen_url = "https://finviz.com/screener.ashx?v=111&f=cap_midover,fa_eps5years_o5,fa_epsyoy_o10,fa_epsyoy1_o5,fa_estltgrowth_pos,fa_netmargin_o5,fa_pe_profitable,fa_sales5years_o5,geo_usa,ta_sma200_pa&ft=4&o=sector"

yahoo_q_url = "https://finance.yahoo.com/quote/%s"
yahoo_holdings_url = "https://finance.yahoo.com/quote/%s/holdings/"
yahoo_hp_url =  "https://finance.yahoo.com/quote/%s/history/"
yahoo_perf_url = "https://finance.yahoo.com/quote/%s/performance/"
yahoo_risk_url = "https://finance.yahoo.com/quote/%s/risk/"

bbg_quote_url = "https://www.bloomberg.com/quote/%s:US"

dropbox_stocklist_url = "https://www.dropbox.com/s/efo19cicf604oxl/stock.txt"
dropbox_fundlist_url = "https://www.dropbox.com/s/t7wfkzq85u13c43/fund.txt"
dropbox_explist_url = "https://www.dropbox.com/s/3pz48x1x53h0nz7/exp.txt"

mw_annual_url = "https://www.marketwatch.com/investing/stock/%s/financials"
mw_quarterly_url = "https://www.marketwatch.com/investing/stock/%s/financials/income/quarter"

mkt_index = {'DIA': 1, 'VOO': 1, 'ONEQ': 1, 'VIXM': 1}
