'''
Created on Nov 19, 2017

@author: Aaron
'''
from context import constants

def gen_summary_html(symbol_lst):
    html_str = '<html><head>'
    html_str += '<body><table>'
    
    for symbol_dict in symbol_lst:
        html_str += '<tr>'
        html_str += '<td><a href=\"%s\">%s</a> |' % (symbol_dict['Url'], symbol_dict['Symbol'])
        html_str += ' | %s |' % symbol_dict['Company']
        html_str += ' | %s |' % symbol_dict['Sector']
        html_str += ' | %s |' % symbol_dict['Industry']
        html_str += ' | %s |' % symbol_dict['Change']
        html_str += ' | %s ' % symbol_dict['Volume']
        html_str += '</td></tr>'
        img_src = constants.finviz_img_url % symbol_dict['Symbol']
        html_str += '<tr><td><img src=' + img_src
        html_str += ' width="75%" height="75%"/></td></tr>'
        
    html_str += '</table></body></head></html>'
    return html_str
