#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 21:26:53 2018

@author: mecit
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

import time


co = webdriver.ChromeOptions()
co.add_argument("log-level=3")
co.add_argument("--headless")

def get_proxies(co=co):
    driver = webdriver.Chrome(chrome_options=co)
    driver.get("https://free-proxy-list.net/")

    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")

        if result[-1] == "yes":
            PROXIES.append(result[0]+":"+result[1])

    driver.close()
    return PROXIES


ALL_PROXIES = get_proxies()


def proxy_driver(PROXIES, co=co):
    prox = Proxy()

    if PROXIES:
        pxy = PROXIES[-1]
    else:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()

    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = pxy
    prox.socks_proxy = pxy
    prox.ssl_proxy = pxy

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(chrome_options=co, desired_capabilities=capabilities)

    return driver

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
    
    # code must be in a while loop with a try to keep trying with different proxies
    running = True
    
    while running:
        try:
            # create a new session
            p_driver = proxy_driver(ALL_PROXIES)

            irand = randrange(15, 30)
            p_driver.implicitly_wait(irand)
            p_driver.get(url)
            
            #Selenium hands the page source to Beautiful Soup
            soup_level1=BeautifulSoup(p_driver.page_source, 'html.parser')
            
            data = soup_level1.find(attrs={'id': 'gs_res_ccl'}).text.split("Cited by")[1]
            if data !=None:
                datalist[tmp] = data.split()[0]
                print(tmp, datalist[tmp])
            #end the Selenium browser session
            p_driver.quit()
            
            # if statement to terminate loop if code working properly
            running = False
            
            # you 
        except:
            new = ALL_PROXIES.pop()
            
            # reassign driver if fail to switch proxy
            p_driver = proxy_driver(ALL_PROXIES)
            print("--- Switched proxy to: %s" % new)
            time.sleep(5)



