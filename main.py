'''
Created on Nov 10, 2017

@author: Aaron
'''
from view import view
from tools import dateutil

if __name__ == '__main__':
    if dateutil.can_run():
        view.screen_daily()
        view.track_stocklist()
        view.track_fundlist()
