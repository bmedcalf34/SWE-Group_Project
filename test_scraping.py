# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 17:26:14 2021

@author: maryam botrus 
"""

import requests 
from bs4 import BeautifulSoup 
    
def getdata(url): 
    r = requests.get(url) 
    return r.text 
    
htmldata = getdata("http://www.BettyCrocker.com/recipes/grilled-peppercorn-t-bones/f4513f7b-c408-4052-b560-94f60d6ed7b7") 
soup = BeautifulSoup(htmldata, 'html.parser')
my_list = []
try:
    
    for item in soup.find_all('img'):
        #print(item['src'])
        my_list.append(item['src'])
except:
    print('Some bad urls')
    
for elem in my_list:
    print(elem)