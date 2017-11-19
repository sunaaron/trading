'''
Created on Nov 11, 2017

@author: Aaron
'''
import json

def get_conf():
    with open ("./conf.json", "r") as f:
        return json.loads(f.read())
    
def get_multiplier(unit):
    return {
        'B': 1000000000,
        'M': 1000000,
    }[unit]