'''
Created on Nov 10, 2017

@author: Aaron
'''
from bs4 import BeautifulSoup
from datetime import datetime
from model import DailySummary, HistorySummary, Symbol

def process_screen_list_tr(tr):
    td_lst = tr.find_all('td', {'class': 'screener-body-table-nw'})
    symbol = td_lst[1].find('a').text
    url = "%s%s" %("http://finviz.com/", td_lst[1].find('a').get("href"))
    company = td_lst[2].text
    sector = td_lst[3].text
    industry = td_lst[4].text
    change = td_lst[9].text
    volume = td_lst[10].text
    return {'Symbol': symbol, 
            'Url': url, 
            'Company': company, 
            'Sector': sector, 
            'Industry': industry, 
            'Change': change, 
            'Volume': volume}

def parse_screen_list_from_finviz(raw_content):
    content = BeautifulSoup(raw_content, "html.parser")
    odd_tr_lst = content.find_all('tr', {'class': 'table-dark-row-cp'})
    even_tr_lst = content.find_all('tr', {'class': 'table-light-row-cp'})

    symbol_lst = []
    for tr in odd_tr_lst:
        symbol_lst.append(process_screen_list_tr(tr))
    for tr in even_tr_lst:
        symbol_lst.append(process_screen_list_tr(tr))
    return symbol_lst

def parse_symbol_details_from_finviz(symbol, raw_content):
    table = BeautifulSoup(raw_content, "html.parser").findAll(
                            "table", {"class": "snapshot-table2"})
    attr_tds = table[0].findAll("td", {"class": "snapshot-td2-cp"})
    value_tds = table[0].findAll("td", {"class": "snapshot-td2"})
    
    attr_dict = {}
    for i in xrange(len(attr_tds)):
        attr = attr_tds[i].text
        value = value_tds[i].text
        attr_dict[attr] = value
    return Symbol(symbol=symbol, 
                  attr_dict=attr_dict)

def parse_historical_prices_from_yahoo(symbol, raw_content):
    """
    Close prices only
    """
    data = []
    rows = BeautifulSoup(raw_content, "html.parser").findAll('table')[0].tbody.findAll('tr')

    for each_row in rows:
        divs = each_row.findAll('td')
        if divs[1].span.text != 'Dividend': #Ignore this row in the table
            d_summary = DailySummary(
                dt=datetime.strptime(divs[0].span.text, '%b %d, %Y'),
                op=float(divs[1].span.text.replace(',','')),
                cp=float(divs[4].span.text.replace(',','')),
                vol=float(divs[6].span.text.replace(',','')),
            )

            data.append(d_summary)
    
    return HistorySummary(
            symbol=symbol,
            d_sums=data[::-1]
            )


def parse_historical_prices_from_pandas(symbol, pandas_data):
    date_lst = pandas_data.index.to_pydatetime().tolist()
    open_lst = pandas_data['Open'].values.tolist()
    close_lst = pandas_data['Close'].values.tolist()
    volume_lst = pandas_data['Volume'].values.tolist()
    
    data = []
    for i in xrange(len(date_lst)):
        d_summary = DailySummary(
                dt=date_lst[i],
                op=open_lst[i],
                cp=close_lst[i],
                vol=volume_lst[i],
            )
        data.append(d_summary)
    
    return HistorySummary(
            symbol=symbol,
            d_sums=data
            )
    
def parse_watchlist_from_dropbox():
    watchlist_path = "./watchlist.txt"
    watchlist_file = open(watchlist_path, "r")
    watchlist = watchlist_file.read().split("\n")
    return [wl.rstrip('\r') for wl in watchlist]

