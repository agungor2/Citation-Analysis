#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 14:44:13 2018

@author: mecit
"""
columns = ['paperTitle','authors', 'year','venue','index','idReference','abstract']
the_file = 'outputacm.txt'
lines = open(the_file).read().splitlines()
read_file = {}
#Read the first line
tmp_read_file={}
for i in range(1,len(lines)):  # start=17, stop=None
    line = lines[i]
    if line != '':
        if line[1]=="*":
            tmp_read_file[columns[0]] = line[2:len(line)]
        elif line[1]=="@":
            tmp_read_file[columns[1]] = line[2:len(line)]
        elif line[1]=="t":
            tmp_read_file[columns[2]] = line[2:len(line)]
        elif line[1]=="c":
            tmp_read_file[columns[3]] = line[2:len(line)]
        elif line[1:6]=="index":
            tmp_read_file[columns[4]] = line[6:len(line)]
        elif line[1]=="%":
            tmp_read_file[columns[5]] = line[2:len(line)]
        elif line[1]=="!":
            tmp_read_file[columns[6]] = line[2:len(line)]
            
    if line =='':
        read_file[int(tmp_read_file[columns[4]])] = tmp_read_file
        del tmp_read_file
        tmp_read_file = {}
    
    
###############################################################################
#after read the file do the web search to extract the citation number

import requests ; from bs4 import BeautifulSoup

all_citation_count = {}
for i in range(421,len(read_file)):
    search_item = read_file[i]['paperTitle']
    url = "http://www.google.com/search?client=ubuntu&channel=fs&q="+ '+'.join(search_item.split()) + '%7D&ie=utf-8&oe=utf-8'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")
    
    # Take out the <div> of name and get its value
    name_box = soup.find(attrs={'class': 'f'})
    
    if name_box != None:
        name = name_box.text.strip() # strip() is used to remove starting and trailing
        
        if "Cited" in name:
            citation_count = int(name.split("Cited by")[1])
            all_citation_count[search_item] = citation_count
            print(i)
            print(search_item)
            print(citation_count)
            print('\n')
    