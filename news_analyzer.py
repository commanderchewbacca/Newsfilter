import json
import requests
import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
sys.path.append('Stanford-NER-Python/main.py')
import main
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='b5881e7fff63474b8680919402a7e437')

#todo
'''
    1)use spacy form matrix
    2)use flame 
    3)upload articles to server
'''


def get_headlines():
    top_headlines = newsapi.get_top_headlines(sources='fox-news, cnn')
    if top_headlines.get('status'):
        articles = top_headlines['articles']


        print(articles)
def common_analyze(stringa, stringb):


    # # count will contain all the word counts
    # count = {}
    #
    # # insert words of string A to hash
    # for word in stringa.split():
    #     count[word] = count.get(word, 0) + 1
    #
    # # insert words of string B to hash
    # for word in stringb.split():
    #     count[word] = count.get(word, 0) + 1
    #
    # # return required list of words
    # total_count = 0
    # for word in count:
    #     count[word] > 1
    #     total_count += 1
    # return total_count




get_headlines()