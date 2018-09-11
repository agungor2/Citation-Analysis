# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
filenames = glob.glob('*.xml')

#Read through one by one and parse it
all_papers = []
for xml_file in filenames:
    tree = xml.etree.ElementTree.parse(xml_file)
    root = tree.getroot()
    
    xmlstr = xml.etree.ElementTree.tostring(root, encoding='utf-8', method='xml')
    temporary_dict = make_dict_from_tree(xml.etree.ElementTree.fromstring(xmlstr))
    
    journal_list = ["Nature",
                    "Science",
                    "Proceedings of the National Academy of Sciences of the United States of America"]
    for i in range(len(temporary_dict["PubmedArticleSet"]["PubmedArticle"])):
        tmp = {}
        if ("Abstract" in temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"] and 
        "ArticleTitle" in temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"] and 
        "Year" in temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"] and 
        temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["Title"] in journal_list):
            tmp["ArticleTitle"] = temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"]
            tmp["Abstract"] = temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
            tmp["Pub_Year"] = temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"]
            tmp["MeshHeading"] = temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["MeshHeadingList"]["MeshHeading"]
            tmp["Venue"] = temporary_dict["PubmedArticleSet"]["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["Title"]
            all_papers.append(tmp)
    print xml_file
    print len(all_papers)