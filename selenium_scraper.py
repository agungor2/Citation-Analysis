#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 16:18:06 2018

@author: mecit
"""
"""
https://scholar.google.com/scholar?hl=en&as_sdt=0%2C38&q=Bayesian+multiple+instance+learning%3A+automatic+feature+selection+and+inductive+transfer&btnG=
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from random import randrange

article_names = pd.read_csv("articlenames.csv")
datalist = {} #empty list
#launch url
main_website = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C38&q="
main_website_addition = "&btnG="
for i in range(len(article_names)):
    tmp = re.sub(r'[^\w\s]','',article_names["ArticleTitle"].iloc[i])
    url = main_website + '+'.join(tmp.split()) + main_website_addition
    
    # create a new Firefox session
    driver = webdriver.Firefox()

    # randrange gives you an integral value
    irand = randrange(30, 60)
    driver.implicitly_wait(irand)
    driver.get(url)
    
    #Selenium hands the page source to Beautiful Soup
    soup_level1=BeautifulSoup(driver.page_source, 'html.parser')
    
    data = soup_level1.find(attrs={'id': 'gs_res_ccl'}).text.split("Cited by")[1]
    if data !=None:
        datalist[tmp] = data.split()[0]
        print(tmp, datalist[tmp])
    #end the Selenium browser session
    driver.quit()