import json
import requests
import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
import spacy

from FLAME import FLAME
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

        print(articles)

    matrix = [[0] * len(articles)] * len(articles)
    print(matrix)
    analayze_headlines_DBSCAN(matrix, articles)


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





get_headlines()
