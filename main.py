'''
Created on Nov 10, 2017

@author: Aaron
'''
from context import constants
from tools import dateutil, misc
from view import view


if __name__ == '__main__':
    if dateutil.can_run():
        print misc.timer(view.track_fundlist,
                         constants.dropbox_fundlist_url)
