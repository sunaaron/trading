'''
Created on Nov 10, 2017

@author: Aaron
'''
from bs4 import BeautifulSoup
from datetime import datetime
from ioutil import diskman
from model import DailySummary, HistorySummary, Symbol
from tools import fetcher

def process_screen_list_tr(tr):
    td_lst = tr.find_all('td', {'class': 'screener-body-table-nw'})
    symbol = td_lst[1].find('a').text
    company = td_lst[2].text
    sector = td_lst[3].text
    industry = td_lst[4].text
    market = td_lst[6].text
    change = td_lst[9].text
    volume = td_lst[10].text
    screen_dict = {'Symbol': symbol, 
                   'Company': company, 
                   'Sector': sector, 
                   'Industry': industry,
                   'Market': market, 
                   'Change': change, 
                   'Volume': volume,
                   }
    symbol_obj = Symbol(symbol=symbol)
    symbol_obj.screen_dict = screen_dict
    return symbol_obj 

def parse_screen_list_urls_from_finviz(raw_content):
    content = BeautifulSoup(raw_content, "html.parser")
    a_lst = content.find_all('a', {'class': 'screener-pages'})
    urls = ["https://finviz.com/%s" % a["href"] for a in a_lst]
    return urls

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

def parse_symbol_attr_dict_from_finviz(symbol_str, raw_content):
    """
    this function returns attr_dict
    """
    table = BeautifulSoup(raw_content, "html.parser").findAll(
                            "table", {"class": "snapshot-table2"})
    attr_tds = table[0].findAll("td", {"class": "snapshot-td2-cp"})
    value_tds = table[0].findAll("td", {"class": "snapshot-td2"})
    
    attr_dict = {}
    for i in xrange(len(attr_tds)):
        attr = attr_tds[i].text
        value = value_tds[i].text
        attr_dict[attr] = value

    td_lst = BeautifulSoup(raw_content, "html.parser").findAll(
                "td", {"class": "fullview-links"})
    a_lst = td_lst[1].findAll("a")
    attr_dict["Sector"] = a_lst[0].text
    attr_dict["Industry"] = a_lst[1].text
    
    return attr_dict
    
def parse_symbol_details_from_finviz(symbol_str, raw_content):
    """
    this function returns a Symbol object directly
    """
    attr_dict = parse_symbol_attr_dict_from_finviz(symbol_str, raw_content)
    symbol_obj = Symbol(symbol=symbol_str)
    symbol_obj.attr_dict = attr_dict
    return symbol_obj

def parse_stmt_from_mw(symbol_str, raw_content):
    tr_sales = BeautifulSoup(raw_content, "html.parser").findAll(
                            "tr", {"class": "partialSum"})
    td_sales = tr_sales[0].findAll("td", {"class": "valueCell"})
    sales = [td.text for td in td_sales if td.text != '-']
    
    tr_income = BeautifulSoup(raw_content, "html.parser").findAll(
                            "tr", {"class": "totalRow"})
    td_income = tr_income[0].findAll("td", {"class": "valueCell"})
    income = [td.text for td in td_income if td.text != '-']
    return sales, income

def parse_historical_prices_from_yahoo(symbol_str, raw_content):
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
            symbol=symbol_str,
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
    
def parse_stock_watchlist_from_dropbox():
    return diskman.load_symbol_as_object("stock.txt")

def parse_fund_watchlist_from_dropbox():
    watchlist_file = open("fund.txt", "r")
    symbol_lst = []
    for line in watchlist_file:
        line_lst = line.split('-')
        symbol_str = line_lst[0].rstrip(' ')
        symbol_desc = line_lst[1].lstrip(' ')
        symbol_obj = Symbol(symbol_str)
        symbol_obj.desc = symbol_desc
        symbol_lst.append(symbol_obj)
    return symbol_lst

    