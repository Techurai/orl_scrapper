#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

data = []

def search_or (search_type):
    month = '3'
    day = '10'
    year = '1981'
    url = f'http://www.oregonliquorsearch.com/servlet/WelcomeController?selMonth={month}&selDay={day}&selYear={year}&btnSubmit=Enter+Site'

    s = requests.Session()
    r = s.get(url)

    search_type = search_type.upper()
    ardbeg_url = f'http://www.oregonliquorsearch.com/servlet/FrontController?view=productlist&action=display&productSearchParam={search_type}&column=Description'
    r = s.get(ardbeg_url)

    soup = BeautifulSoup(r.content, features="lxml")
    table = soup.find('table', {'class':'list'})
    first_check = [item for item in table.find_all('th')]
    first_check = first_check[0].text
    return table

def parse_table (table):
    title_row = [title.text for title in table.find_all('th')]
    data.append(title_row)

    each_item = [item for item in table.find_all('tr') if item.find('td')]
    for child in each_item:
        li = [each.text for each in child.find_all('td') if each.text]
        data.append(li)

search_var = 'ardbeg'
search_table = search_or(search_var)
print(search_table)
# parse_table(search_table)

# for bottle in data:
#     print(bottle[7], '-', bottle[1])