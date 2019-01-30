#Read the Nature articles page to list out all nature publications
import requests ; from bs4 import BeautifulSoup
import os
from tqdm import tqdm
url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
    
response = requests.get(url)
html = BeautifulSoup(response.text, 'html.parser')

list_of_gz_files = []

for i in range(len(html.select('a'))):
    if i%3 ==1:
        list_of_gz_files.append(html.select('a')[i].text)

for document in tqdm(list_of_gz_files):
    #DEfine url for every file
    zipurl = url + document
    resp = requests.get(zipurl)
    
    # assuming the subdirectory tempdata has been created:
    zname = os.path.join('/home/mecit/Desktop/Citation-Analysis/tempdata', document)
    zfile = open(zname, 'wb')
    zfile.write(resp.content)
    zfile.close()