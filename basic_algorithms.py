"""
CS 121: Analyzing Election Tweets

Yujing Sun

Basic algorithms module

Algorithms for efficiently counting and sorting distinct 'entities',
or unique values, are widely used in data analysis.
"""

import math
from util import sort_count_pairs

# Task 1.1
def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens.

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''
    count_token = {}
    for token in tokens:
        if token not in count_token.keys():
            count_token[token] = 0
        count_token[token] += 1
    return count_token


# Task 1.2
def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens.

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''

    #Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    dic_tokens = count_tokens(tokens)
    pairs = list(dic_tokens.items())
    sort_pairs = sort_count_pairs(pairs)
    if len(sort_pairs) <= k:
        k = len(sort_pairs)
    top_k = [sort_pairs[i][0] for i in range(k)]
    return top_k


# Task 1.3
def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times.

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''

    #Error checking (DO NOT MODIFY)
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")

    dic_tokens = count_tokens(tokens)
    pairs = list(dic_tokens.items())
    sort_pairs = sort_count_pairs(pairs)
    min_set = set()
    for pair in sort_pairs:
        if pair[1] >= min_count:
            min_set.add(pair[0])
    return min_set


# Task 1.4

def idf(docs):
    '''
    Compute idf for each token.

    Inputs:
      docs: list of list of tokens

    Returns: a dictionary for idf
    '''

    all_t = set()
    for doc in docs:
        all_t = all_t.union(set(doc))
    idf_dic = {}
    for t in all_t:
        for doc in docs:
            if t in set(doc):
                idf_dic[t] = idf_dic.get(t,0) + 1
    idf1 = {key:math.log(len(docs)/value) for key,value in idf_dic.items()}
    return idf1

def tf_doc(docs):
    '''
    Compute tf for each token.

    Inputs:
      docs: list of list of tokens

    Returns: a lst of dictionary of tf
    '''
    tf_lst = []
    for doc in docs:
        if doc == []:
            tf_lst.append({})
        else:
            count_token = count_tokens(doc)
            max_doc = count_token[find_top_k(doc, 1)[0]]
            tf_lst.append({k:0.5+0.5*v/max_doc for k,v in count_token.items()})
    return tf_lst

def tf_idf(docs):
    '''
    Compute tf*idf for each token.

    Inputs:
      docs: list of list of tokens

    Returns: a lst of dictionary of tf*idf
    '''
    tf_docs = tf_doc(docs)
    idf_docs = idf(docs)
    tfidf = []
    for dic in tf_docs:
        tfidf.append({key: value*idf_docs[key] for key, value in dic.items()})
    return tfidf

def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''
    tf_idf_dic = tf_idf(docs)
    salient = []
    for dic in tf_idf_dic:
        salient.append({key for key,value in dic.items() if value > threshold})
    return salient
