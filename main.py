'''
Created on Nov 10, 2017

@author: Aaron
'''
from tools import misc
from view import view
from tools import dateutil


if __name__ == '__main__':
    if dateutil.can_run():
        print misc.timer(view.track_fundlist)
