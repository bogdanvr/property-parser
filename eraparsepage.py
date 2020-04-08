# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 22:58:11 2019

@author: taisiya
"""

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import ssl
from datetime import datetime
import time
from random import randint
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
    
    try:
        #url = 'http://www.eraworld.ru'
        
        html = urlopen(url, context=ctx)
    
        
    except HTTPError:
        return print('no html')
    try:
        bsobj = bs(html, 'html.parser')
    except HTTPError:
        return print('no bsobj')
    
    
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
    
    
            
            
#i = 'http://www.eraworld.ru/catalog/32207'
            
#get_page(i)          
            
       
    #try:
     #   for i in bsobj.find_all('div', {'class':'bxr-element-image'}):
      #      img = i.find('img').attrs['src']
       #     link = i.find('a').attrs['href']
        #    
         #   if img not in images:
          #      images.add(img)
           #     link_img.add('{} - {}'.format(link,img))
  #  except AttributeError:
   #     print('No img')



with open('urlera.txt') as f:
    st = f.readlines()
    
st = st[0].split('http://www.eraworld.ru')
print(len(st))

#get_page('/catalog/puskateli_kontaktory_i_rele/rele_elektroteplovoe_rtn_5372_110_135a_tdm/')

     
for i in st:
    count += 1
    print(count)
    get_page('http://www.eraworld.ru'+i)
    time.sleep(1)



                
"""  

html = urlopen('https://www.electrostyle.org/catalog/schetchiki_elektroenergii/', context=ctx)
bsobj = bs(html, 'html.parser')
try:
    if bsobj.find('div', {'class':'promo'}):
        print('Find text')
    else:
        print('No text')
except AttributeError:
        print('No text')
"""

#import eraparspage


df = pd.DataFrame({'Data':[10, 20, 30, 20, 15, 30, 45], 'Date':[25,36,78,32,99,14,23] })

dfd = pd.DataFrame({'name':['fonar', 'zazhim'], 'garant':[5, 4], 'massa':[0.14, 0.12], 'napr':[1, 10]})



writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')


df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

dd = {}



 
s = [list(i) for i in pp]
k = set()

for i in s:
    for t in i:
        
        k.add(t)
klist = list(k)
print('klist =', klist)

"""
for i in klist:
    dd[i] = [ x[i] for x in m]
"""

for i in klist:
    dd[i] = [ x.get(i) for x in pp]
    
    
    
print(dd)

df2 = pd.DataFrame(dd)
print(df2)


writer = pd.ExcelWriter('pandas_simple7.xlsx', engine='xlsxwriter')


df2.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
    
