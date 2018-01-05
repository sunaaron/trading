'''
Created on Jan 4, 2018

@author: Aaron
'''
def red(text):
    return "<strong style=\"color: red;\">%s</strong>" % text

def green(text):
    return "<strong style=\"color: green;\">%s</strong>" % text

def orange(text):
    return "<strong style=\"color: orange;\">%s</strong>" % text

def rank_change_html(rank_change):
    if rank_change == 'N/A':
        return rank_change
    if rank_change > 0:
        return green('+' + str(rank_change))
    if rank_change == 0:
        return orange(str(rank_change))
    return red(str(rank_change))
