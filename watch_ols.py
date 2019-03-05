#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

data = []


def search_or(search_type):
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
    table = soup.find('table', {'class': 'list'})
    first_check = [item for item in table.find_all('th')]
    try:
        if first_check[0].text == 'Item Code':
            response = parse_table(table)
        elif first_check[0].text == 'Store No':
            table = soup.find('table', {'id': 'product-details'})
            response = parse_item(table)
    except:
        response = 'ERROR'

    return response


def parse_table(table):
    title_row = [title.text for title in table.find_all('th')]
    data.append(title_row)

    each_item = [item for item in table.find_all('tr') if item.find('td')]
    for child in each_item:
        li = [each.text for each in child.find_all('td') if each.text]
        data.append(li)
    
    response = 'Data processed'
    return response

def parse_item(table):
    title_list = ['Item Code', 'Description', 'Liquor Category', 'Size', 'Proof', 'Age', 'Case Price', 'Bottle Price']

    each_item = table.find('h2').text
    parts = each_item.split(': ')
    name = str(parts[1])
    item_code = parts[0].split(' ')
    
    each_item_info = table.find_all('td')
    li_info = [each.text for each in each_item_info]
    li = [item_code[1], name, li_info[1], li_info[3], li_info[5], ' ', li_info[4], li_info[6]]
    data.append(title_list)
    data.append(li)

    response = 'Data processed'
    return response


search_var = 'wolfburn'
search_table = search_or(search_var)
print(data)

# for bottle in data:
#     print(bottle[7], '-', bottle[1])
