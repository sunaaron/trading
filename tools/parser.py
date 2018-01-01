'''
Created on Nov 10, 2017

@author: Aaron
'''
from bs4 import BeautifulSoup
from datetime import datetime
from ioutil import diskman
from model.symbol import DailySummary, HistorySummary
from model.stock_symbol import StockSymbol
from model.fund_symbol import FundSymbol

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
    # screen is only used for StockSymbol
    symbol_obj = StockSymbol(symbol=symbol)
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

def parse_attr_dict_from_finviz(raw_content):
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
    
def parse_stmt_from_mw(raw_content):
    tr_sales = BeautifulSoup(raw_content, "html.parser").findAll(
                            "tr", {"class": "partialSum"})
    sales, income = [], []
    if len(tr_sales) > 0:
        td_sales = tr_sales[0].findAll("td", {"class": "valueCell"})
        sales = [td.text for td in td_sales if td.text != '-']

    tr_income = BeautifulSoup(raw_content, "html.parser").findAll(
                            "tr", {"class": "totalRow"})
    if len(tr_income) > 0:
        td_income = tr_income[0].findAll("td", {"class": "valueCell"})
        income = [td.text for td in td_income if td.text != '-']
    return sales, income

def parse_markets_from_cnn(raw_content):
    index_dict = {}
    ul = BeautifulSoup(raw_content, "html.parser").\
        select('ul[class*="three-equal-columns"]')
    lis = ul[0].select("li")
    for li in lis:
        spans = li.select("span")
        market = spans[0].text
        change = spans[2].text
        index_dict[market] = change
    return index_dict

def parse_summary_from_yahoo(raw_content):
    summary_dict = {}
    trs = BeautifulSoup(
        raw_content, "html.parser").select('tr[class*="Bxz(bb)"]')
    for tr in trs:
        tds = tr.select("td")
        name = tds[0].text
        value = tds[1].text
        summary_dict[name] = value
    return summary_dict

def parse_holdings_from_yahoo(raw_content):
    holding_dict = {} 
    divs = BeautifulSoup(
        raw_content, "html.parser").select('div[class*="Bdbw(1px)"]')
    for div in divs:
        spans = div.select("span")
        attr = spans[0].text
        value = spans[3].text
        holding_dict[attr] = value
    
    holding_lst = []
    trs = BeautifulSoup(
        raw_content, "html.parser").select('tr[class*="Ta(end)"]')
    for tr in trs:
        tds = tr.select("td")
        if len(tds) == 0:
            continue
        name = tds[0].text
        symbol = tds[1].text
        percent = tds[2].text
        holding_lst.append((name, symbol, percent))
    
    holding_dict['holdings'] = holding_lst
    return holding_dict

def parse_perf_from_yahoo(raw_content):
    divs = BeautifulSoup(
        raw_content, "html.parser").select('div[class*="Bdbw(1px)"]')
    perf_dict = {}
    for div in divs:
        spans = div.select("span")
        first_col = spans[0].text
        if first_col.startswith('201'):
            year = first_col
            change = (spans[2].text, spans[3].text)
            perf_dict[year] = change
        if ('-Year') in first_col:
            perf_dict[first_col] = (
                spans[3].text, spans[4].text)
    return perf_dict

def parse_risk_from_yahoo(raw_content):
    def parse_yr_risk(yr_div):
        yr_spans = yr_div.select("span")
        return (yr_spans[0].text, yr_spans[1].text)
    
    risk_dict = {}
    divs = BeautifulSoup(
        raw_content, "html.parser").select('div[class*="Bdbw(1px)"]')
    for div in divs[1:]:
        sub_divs = div.select("div")
        name_div = sub_divs[0]
        name_spans = name_div.select("span")
        name = name_spans[0].text
        risk_dict[name] = {}
        
        yr3_div, yr5_div, yr10_div = sub_divs[1:]
        risk_dict[name]['3-year'] = parse_yr_risk(yr3_div)
        risk_dict[name]['5-year'] = parse_yr_risk(yr5_div)
        risk_dict[name]['10-year'] = parse_yr_risk(yr10_div)
    return risk_dict

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

def parse_historical_prices_from_pandas(symbol_str, pandas_data):
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
            symbol=symbol_str,
            d_sums=data
            )

def parse_summary_from_bbg(raw_content):
    summary_dict = {}
    divs = BeautifulSoup(raw_content, "html.parser").findAll(
                        "div", {"class": "cell"})
    for div in divs:
        cell_label = div.select('div[class="cell__label"]')
        value_label = div.select('div[class*="cell__value"]')
        cell = cell_label[0].text.strip(' ')
        value = value_label[0].text.strip(' ')
        summary_dict[cell] = value
    return summary_dict
    
def parse_stock_watchlist_from_dropbox():
    return diskman.load_symbol_as_object("stock.txt")

def parse_fund_watchlist_from_dropbox(filename):
    watchlist_file = open(filename, "r")
    symbol_lst = []
    for line in watchlist_file:
        if line.startswith('#') or len(line) <= 5:
            continue
        line_lst = line.split('\t')
        symbol_str = line_lst[0].strip(' ')
        symbol_desc = line_lst[1].strip(' \r\n')
        symbol_obj = FundSymbol(symbol_str)
        symbol_obj.desc = symbol_desc
        symbol_lst.append(symbol_obj)
    return symbol_lst

def parse_coef_list_from_dropbox():
    watchlist_file = open('coef.txt', "r")
    coef_lst = []
    for line in watchlist_file:
        line_lst = line.split('\t')
        symbol_str_left = line_lst[0].strip(' ') 
        symbol_str_right = line_lst[1].strip(' \r\n') 
        symbol_obj_left = FundSymbol(symbol_str_left)
        symbol_obj_right = FundSymbol(symbol_str_right)
        coef_lst.append((symbol_obj_left, 
                           symbol_obj_right))
    return coef_lst
