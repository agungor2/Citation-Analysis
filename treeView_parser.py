#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 12:02:29 2019

@author: mecit
"""
"""
import requests ; from bs4 import BeautifulSoup

url = "https://meshb.nlm.nih.gov/treeView"
    
response = requests.get(url)
html = BeautifulSoup(response.text, 'html.parser')
"""

import pandas as pd

treeView_df = pd.read_csv("2019MeShTreeHierarchy.csv")

previous_code = 'A01'
from collections import defaultdict
all_mesh = defaultdict(list)
tmp_mesh = 'Body Regions'
for i in range(len(treeView_df)):
    tmp_code = treeView_df.iloc[i].values[0].split()[0]
    current_code = tmp_code.split('.')[0]
    if previous_code == current_code:
        all_mesh[tmp_mesh].append(" ".join(treeView_df.iloc[i].values[0].split()[1:]))
    else:
        previous_code = current_code
        tmp_mesh = " ".join(treeView_df.iloc[i].values[0].split()[1:])
        all_mesh[tmp_mesh].append(" ".join(treeView_df.iloc[i].values[0].split()[1:]))

two_level_tree = pd.read_csv("Pubmed_TreeView.csv", header=None, names = ["First", "Second"])
all_mesh_list = []
all_mesh_list = [element for element in all_mesh.keys()]

bottom2top = defaultdict(list)

for i in range(len(two_level_tree)):
    first_tmp = " ".join(two_level_tree["First"].iloc[i].split()[0:-1])
    second_tmp = " ".join(two_level_tree["Second"].iloc[i].split()[0:-1])
    bottom2top[second_tmp] = first_tmp

###########################################################################################
top_tree_mesh_list= {
"A": "Anatomy",

"B": "Organisms",

"C": "Diseases",

"D": "Chemicals and Drugs",

"E": "Analytical, Diagnostic and Therapeutic Techniques, and Equipment",

"F": "Psychiatry and Psychology",

"G": "Phenomena and Processes",

"H": "Disciplines and Occupations",

"I": "Anthropology, Education, Sociology, and Social Phenomena",

"J": "Technology, Industry, and Agriculture",

"K": "Humanities",

"L": "Information Science",

"M": "Named Groups",

"N": "Health Care",

"V" : "Publication Characteristics",

"Z": "Geographicals"

}

"""Create bottom to top list of Mesh List

"""
bottom2top_all_mesh = defaultdict(dict)

previous_code = 'A01'
from collections import defaultdict
tmp_mesh = 'Body Regions'
for i in range(len(treeView_df)):
    tmp_code = treeView_df.iloc[i].values[0].split()[0]
    current_code = tmp_code.split('.')[0]
    current_top_tree = treeView_df.iloc[i].values[0].split()[0].split('.')[0][0]
    at = {}
    if previous_code == current_code:
        at[tmp_mesh] = top_tree_mesh_list[current_top_tree]
    else:
        previous_code = current_code
        tmp_mesh = " ".join(treeView_df.iloc[i].values[0].split()[1:])
        at[tmp_mesh] = top_tree_mesh_list[current_top_tree]
        
    bottom2top_all_mesh[" ".join(treeView_df.iloc[i].values[0].split()[1:])] = at
    
    
###################################################################################
"""
Now Search Through all the database
"""

import xml.etree.ElementTree
import glob
def make_dict_from_tree(element_tree):
    """Traverse the given XML element tree to convert it into a dictionary.
    
    :param element_tree: An XML element tree
    :type element_tree: xml.etree.ElementTree
    :rtype: dict
    """
    def internal_iter(tree, accum):
        """Recursively iterate through the elements of the tree accumulating
        a dictionary result.
        
        :param tree: The XML element tree
        :type tree: xml.etree.ElementTree
        :param accum: Dictionary into which data is accumulated
        :type accum: dict
        :rtype: dict
        """
        if tree is None:
            return accum
        
        if tree.getchildren():
            accum[tree.tag] = {}
            for each in tree.getchildren():
                result = internal_iter(each, {})
                if each.tag in accum[tree.tag]:
                    if not isinstance(accum[tree.tag][each.tag], list):
                        accum[tree.tag][each.tag] = [
                            accum[tree.tag][each.tag]
                        ]
                    accum[tree.tag][each.tag].append(result[each.tag])
                else:
                    accum[tree.tag].update(result)
        else:
            accum[tree.tag] = tree.text
        
        return accum
    
    return internal_iter(element_tree, {})

#Collect all xml file names
filenames = glob.glob('/home/mecit/Desktop/Citation-Analysis/tempdata/*.xml')

#Read through one by one and parse it
first_level_list = []
for keys in top_tree_mesh_list:
    first_level_list.append(top_tree_mesh_list[keys])
all_papers = []
count = 0
mesh_list_count = {}
for mesh_list in all_mesh_list:
    mesh_list_count[mesh_list] = 0
for xml_file in filenames:
    tree = xml.etree.ElementTree.parse(xml_file)
    root = tree.getroot()
    
    xmlstr = xml.etree.ElementTree.tostring(root, encoding='utf-8', method='xml')
    temporary_dict = make_dict_from_tree(xml.etree.ElementTree.fromstring(xmlstr))
    
    for i in range(len(temporary_dict["PubmedArticleSet"]["PubmedArticle"])):
        tmp = {}
        if ("Abstract" in temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"] and 
        "ArticleTitle" in temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"] and 
        "Year" in temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"] and
        "MeshHeadingList" in temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"] and
        "MeshHeading" in temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["MeshHeadingList"]):
            if (int(temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"]) >= 1990):
                tmp["ArticleTitle"] = temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"]
                tmp["Abstract"] = temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
                tmp["Pub_Year"] = temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"]
                tmp_mesh2 = temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["MeshHeadingList"]["MeshHeading"]
                if len(tmp_mesh2) > 1 and type(tmp_mesh2) is list:
                    list_of_mesh_list = []
                    for j in range(len(tmp_mesh2)):
                        if "DescriptorName" in tmp_mesh2[j]:
                            tmp_mesh3 = tmp_mesh2[j]['DescriptorName']
                            if tmp_mesh3 in bottom2top_all_mesh:
                                if bottom2top_all_mesh[tmp_mesh3] not in list_of_mesh_list:
                                    list_of_mesh_list.append(bottom2top_all_mesh[tmp_mesh3])
                    if len(list_of_mesh_list) > 0:
                        #think about the case if there is more chance of being categorized in the different meshHeadings
                        MeshHeading_Level2 = []
                        MeshHeading_Level1 = []
                        for k in range(len(list_of_mesh_list)):
                            if list(list_of_mesh_list[k].keys())[0] not in MeshHeading_Level2:
                                MeshHeading_Level2.append(list(list_of_mesh_list[k].keys())[0]) 
                            if list_of_mesh_list[k][list(list_of_mesh_list[k].keys())[0]] not in MeshHeading_Level1:
                                MeshHeading_Level1.append(list_of_mesh_list[k][list(list_of_mesh_list[k].keys())[0]])
                        for l in first_level_list:
                            key_name_1 = "Level 1 : " + l
                            if l in MeshHeading_Level1:
                                tmp[key_name_1] = 1
                            else:
                                tmp[key_name_1] = 0
                        for m in all_mesh_list:
                            key_name_2 = "Level 2 : " + m
                            if m in MeshHeading_Level2:
                                tmp[key_name_2] = 1
                            else:
                                tmp[key_name_2] = 0
                        
                        for n in mesh_list_count:
                            if n in MeshHeading_Level2:
                                mesh_list_count[n] += 1
                        if any(mesh_list_count[o] < 15000 for o in MeshHeading_Level2):
                            all_papers.append(tmp)
    print(xml_file)
    count += 1
    print(len(all_papers), count)
    #if count > 20:
    #    break;
at = pd.DataFrame(all_papers)
at.to_csv("Paper_List.csv", encoding='utf-8', index=False)