'''
Created on Nov 10, 2017

@author: Aaron
'''
from view import view
from tools import dateutil

if __name__ == '__main__':
#     dateutil.can_do_screen() and view.screen_new()
    dateutil.can_do_stock_track() and view.track_stocklist()
    dateutil.can_do_fund_track() and view.track_fundlist()
