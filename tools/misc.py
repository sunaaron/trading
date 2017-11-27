'''
Created on Nov 11, 2017

@author: Aaron
'''
from context import constants
import json

def get_conf():
    with open ("./conf.json", "r") as f:
        return json.loads(f.read())
    
def get_multiplier(unit):
    return {
        'B': 1000000000,
        'M': 1000000,
        'K': 1000,
    }[unit]
    
def build_finviz_screen_movement_url():
    base_url = constants.finviz_screen_url
    url_lst = base_url.split(",")
    # relative volume 1.5
    url_lst.insert(-2, "sh_relvol_o1.5")
    # trend going up
    url_lst.insert(-2, "ta_change_u")
    return ",".join(url_lst)
