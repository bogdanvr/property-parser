# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 22:58:11 2019

@author: bogdan
"""
"""
scraper for the automatic collection of product properties from the supplier’s website.
Unloading properties in excel, in a format for automatic loading in 1C
"""
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.error import HTTPError
import ssl
from datetime import datetime
import time
import pandas as pd
now = datetime.now()
date = str(now).split(' ')[0]






ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

count = 0

images = set()
text = 0
pages = set()
h1 = set()
promo = set()
link_img = set()
nostock = set()
prod = {}
pp = []


def get_page(url):
    global pages
    global text
    global h1
    global promo
    global images
    global link_img
    global count
    global nostock
    global prod
    global pp
    
    # try to get url
    try:
        
        
        html = urlopen(url, context=ctx)
        #url = 'http://www.eraworld.ru'
        
    except HTTPError:
        return print('no html')
    
    #try to get html
    try:
        bsobj = bs(html, 'html.parser')
    except HTTPError:
        return print('no bsobj')
    
    # try to get header h1 and vendore code
    try:
        head = bsobj.h1.get_text()
        hs = head.split('  ')
        hd = hs[0].strip()
        artikul = hs[6].strip()
        artikul = artikul.replace('Код товара: ', '')
        h1.add(hd)
        print(hd)
    except AttributeError:
        print('No header')
    
    # try to get properties of the product and add them to the dictionary
    try:
        p = {}
        properties = bsobj.find('div', {'id':'itemProporties'})
        for i in properties.find_all('div', {'class': 'row'}):
            prop = i.find('div', {'class': 'col col-lg-4 col-md-6'}).text
            prop = prop.strip()
            value = i.find('div', {'class': 'col col-lg-8 col-md-6'}).text
            p[prop] = value
        p['name'] = hd
        p['artikul'] = artikul
        pp.append(p)
        
    except:
        print('No properties')
    
    
            
            



# Open the file with categiries for scraping
with open('urlera.txt') as f:
    st = f.readlines()

#remove the domain name    
st = st[0].split('http://www.eraworld.ru')
print(len(st))


# run the scraper on the list
for i in st:
    count += 1
    print(count)
    get_page('http://www.eraworld.ru'+i)
    time.sleep(1)




dd = {}



# Get all the property headers that will be used as table columns
s = [list(i) for i in pp]
k = set()

for i in s:
    for t in i:
        
        k.add(t)
klist = list(k)
print('klist =', klist)


# We get a dictionary in which the key is the name of the property, and the value is a list of all its values

for i in klist:
    dd[i] = [ x.get(i) for x in pp]
    
    
    
print(dd)

# Writing a dictionary in a dataframe Pandas

df2 = pd.DataFrame(dd)
print(df2)


writer = pd.ExcelWriter('pandas_simple7.xlsx', engine='xlsxwriter')


df2.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
    
