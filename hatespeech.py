#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:40:38 2018

@author: mecit
  twitter.com/Tweet_Maker_User_Name/status/447788271175999488
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

all_tweets = pd.read_csv("NAACL_SRW_2016.csv",names=["id","abuse"])
all_tweet_text = []
for i in range(len(all_tweets)):
    url = "http://twitter.com/Tweet_Maker_User_Name/status/" + str(all_tweets["id"].iloc[i])
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    #Magical trick for tweets
    tweet_text = html.find(attrs={'class': 'js-tweet-text-container'}).text
    all_tweet_text.append(tweet_text)