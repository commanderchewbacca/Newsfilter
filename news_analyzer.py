import json
import requests
import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
import spacy

from FLAME import FLAME
import numpy as np

from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='b5881e7fff63474b8680919402a7e437')

#todo
'''
    1)use spacy form matrix
    2)use flame 
    3)upload articles to server
'''

nlp = spacy.load('en_core_web_sm')

def get_headlines():
    top_headlines = newsapi.get_top_headlines(sources='fox-news, cnn')
    if top_headlines.get('status'):
        articles = top_headlines['articles']


        print(articles)


    matrix = [[0]*len(articles)]*len(articles)
    print(matrix)
    analayze_headlines(matrix, articles)
def analayze_headlines(matrix,articles):
    if matrix and matrix[0]:
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                y_title = articles[y].get('title')
                x_title = articles[x].get('title')
                if y_title and x_title:
                    print(y_title,x_title)
                    similarity = nlp(y_title).similarity(nlp(x_title))
                    matrix[y][x] = similarity
                    print(similarity)


    model = FLAME( cluster_neighbors= max(1,len(articles)//5) , iteration_neighbors=max(1,len(articles)//5))
    membership = model.fit_predict(np.array(matrix))
    print(matrix)
    print(membership)






get_headlines()