'''
Created on Nov 10, 2017

@author: Aaron
'''
from view import view
from tools import dateutil, fetcher, parser

if __name__ == '__main__':
    raw_content = fetcher.fetch_holdings_from_yahoo("JETS")
    holding_dict, holding_lst = parser.parse_holdings_from_yahoo("JETS", raw_content)
    print holding_dict, holding_lst
#     if dateutil.can_run():
# #         view.screen_daily()
# #         view.track_stocklist()
#         view.track_fundlist()
