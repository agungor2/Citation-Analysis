#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 18:04:12 2018

@author: mecit
"""


"""
Use the following journals:
IEEE Transactions on Information Theory
IEEE Transactions on Signal Processing
international conference on pattern recognition
IEEE Transactions on Communications
IEEE Transactions on Wireless Communications
"""

#Now Read and select the journals
import os, json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics import mean_absolute_error
path_to_json = '/home/mecit/Desktop/Citation Analysis/dblp.v10/dblp-ref'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print(json_files)  # for me this prints ['foo.json']

at2 = [
"IEEE Transactions on Information Theory",
"IEEE Transactions on Signal Processing",
"international conference on pattern recognition",
"IEEE Transactions on Communications",
"IEEE Transactions on Wireless Communications"
       ]

selected_journals = []

for files in json_files:
    data = []
    with open(files) as f:
        for line in f:
            data.append(json.loads(line))
            
    for i in range(len(data)):
        #Check if it is in the selected journal list
        if data[i]['venue'] in at2 and "abstract" in data[i] and "year" in data[i] and "title" in data[i] and "references" in data[i] and data[i]["n_citation"] is not None:
            data[i]['ref_num'] = len(data[i]['references'])
            data[i]['author_num'] = len(data[i]['authors'])
            selected_journals.append(data[i])
            #print(data[i]['venue'])
#Convert it into a dataframe
selected_journals_dataframe = pd.DataFrame(selected_journals)

print(selected_journals_dataframe.columns)
del data, at2, files, json_files, i, line, path_to_json, selected_journals
#Get the overall number of references per paper and number of authors on the paper
selected_journals_dataframe = selected_journals_dataframe.drop('references', 1)
selected_journals_dataframe = selected_journals_dataframe.drop('authors', 1)

#check if all the ids are unique and no repeating article
print(len(selected_journals_dataframe) == len(np.unique(selected_journals_dataframe.id.values)))

selected_journals_dataframe = selected_journals_dataframe.drop('id', 1)
#Combine abstract and title
selected_journals_dataframe['abstract_title'] = selected_journals_dataframe['title'].str.cat(selected_journals_dataframe['abstract'], sep='. ')

#Train test split
train, test = train_test_split(selected_journals_dataframe, test_size=0.3)

#Fit a logistic regression model
# create the transform
vectorizer = HashingVectorizer(n_features=10000)
# encode document
vector = vectorizer.transform(train["abstract_title"])
train_abstract_title = vector.toarray()
#Normalize author number, year, reference number
train_other_features = train[["author_num", "ref_num", "year"]].apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x))).values
train_final = np.concatenate((train_abstract_title, train_other_features), axis=1)
#Do the same steps for test data

vectorizer = HashingVectorizer(n_features=10000)
# encode document
vector = vectorizer.transform(test["abstract_title"])
test_abstract_title = vector.toarray()
#Normalize author number, year, reference number
test_other_features = test[["author_num", "ref_num", "year"]].apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x))).values
test_final = np.concatenate((test_abstract_title, test_other_features), axis=1)

#Apply on Linear Regression
from sklearn.linear_model import LinearRegression
model = LinearRegression(n_jobs=-1)
model.fit(train_final,train["n_citation"].values)
result = mean_absolute_error(test["n_citation"].values, model.predict(test_final))
print("Linear Regression Result: " + str(result))
#Apply on Lasso
from sklearn.linear_model import Lasso
model = Lasso(alpha=0.001)
model.fit(train_final,train["n_citation"].values)
result = mean_absolute_error(test["n_citation"].values, model.predict(test_final))
print("Lasso Regression Result: " + str(result))
#Apply it on Xgboost
from xgboost import XGBRegressor