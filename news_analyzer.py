import json
import requests
import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
import spacy

# from FLAME import FLAME
import numpy as np
from sklearn import cluster

from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='b5881e7fff63474b8680919402a7e437')

# todo
'''
    1)use spacy form matrix
    2)use flame 
    3)upload articles to server
    4) look into dbscan instead
'''

nlp = spacy.load('en_core_web_sm')


def get_headlines():
    top_headlines = newsapi.get_top_headlines(sources='fox-news, cnn')
    if top_headlines.get('status'):
        articles = top_headlines['articles']
    top_headlines = newsapi.get_top_headlines(sources='abc-news')
    if top_headlines.get('status'):
        articles.extend(top_headlines['articles'])
    top_headlines = newsapi.get_top_headlines(sources='bloomberg')
    if top_headlines.get('status'):
        articles.extend(top_headlines['articles'])

        # print(articles)

    # matrix = [[0] * len(articles)] * len(articles)
    # print(matrix)
    # analayze_headlines_DBSCAN(matrix, articles)
    analyze_headlines_setcover(articles)

def analayze_headlines_DBSCAN(matrix, articles):
    if matrix and matrix[0]:
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if y != x:
                    y_title = articles[y].get('title')
                    x_title = articles[x].get('title')
                    if y_title and x_title:

                        # Doing DBSCAN on entities name
                        # y_ent = ""
                        # for i in nlp(y_title).ents:
                        #     y_ent = y_ent + " " + str(i)
                        # x_ent = ""
                        # for i in nlp(x_title).ents:
                        #     x_ent = x_ent + " " + str(i)
                        #
                        # print(y_ent, x_ent)
                        #
                        # similarity = nlp(y_ent).similarity(nlp(x_ent))

                        similarity = nlp(y_title).similarity(nlp(x_title))
                        matrix[y][x] = 1 - similarity
                        print(similarity)
    print(matrix)

    model = cluster.DBSCAN(eps=0.4, min_samples=1, metric="precomputed")
    membership = model.fit_predict(np.array(matrix))
    print(matrix)
    print(membership)
    print([(articles[i].get('title'), membership[i]) for i in range(len(articles))])





def analyze_headlines_setcover(articles):
    print(set(["a","b"]))
    universe = set()
    subsets = []
    groups = []
    categories = []
    for article in articles:
        entities  =  set()
        for i in nlp(article.get('title')).ents:
            entities.add(i.text)
        print(entities)
        subsets.append(entities)
        universe = universe | entities
        groups.append([entities,article])

    cover = set_cover(universe,subsets)
    for cov in cover:
        print("cov",cov)
        categories.append([cov,[]])

    general =set()
    general.add("general")
    categories.append([general,[]])
    print("cata",categories)

    for group in groups:
        max = 0
        maxcount = len(categories)-1
        for count ,catagory in enumerate(categories):
            common = len(catagory[0].intersection(group[0]))

            if common > max:
                max =common
                maxcount = count

        print(maxcount)
        categories[maxcount][1].append(group[1].get('title'))


    for i in categories:
        print(i[0],len(i[1]))
        print(i)








#stolen from http://www.martinbroadhurst.com/greedy-set-cover-in-python.html
def set_cover(universe, subsets):
    """Find a family of subsets that covers the universal set"""
    elements = set(e for s in subsets for e in s)
    # Check the subsets cover the universe
    if elements != universe:
        return None
    covered = set()
    cover = []
    # Greedily add the subsets with the most uncovered points
    while covered != universe:
        subset = max(subsets, key=lambda s: len(s - covered))
        cover.append(subset)
        covered |= subset

    return cover
#stolen from http://www.martinbroadhurst.com/greedy-set-cover-in-python.html

#
# def main():
#     universe = set(range(1, 11))
#     subsets = [set([1, 2, 3, 8, 9, 10]),
#                set([1, 2, 3, 4, 5]),
#                set([4, 5, 7]),
#                set([5, 6, 7]),
#                set([6, 7, 8, 9, 10])]
#     cover = set_cover(universe, subsets)
#     print(cover)


get_headlines()
