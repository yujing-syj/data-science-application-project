"""
CS 121: Analyzing Election Tweets

Yujing Sun

Analyze module

Functions to analyze tweets.
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient

##################### DO NOT MODIFY THIS CODE #####################

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


#####################  MODIFY THIS CODE #####################


############## Part 2 ##############

def combine_tweets(tweets, entity_desc):
    '''
    Combine each tweet together into a list

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.

    Returns: list of tokens (must be immutable)
    '''
    lst = []
    for tweet in tweets:
        key = tweet['entities'][entity_desc[0]]
        for m in key:
            if entity_desc[2]:
                lst.append(m[entity_desc[1]])
            else:
                lst.append(m[entity_desc[1]].lower())
    return lst


# Task 2.1
def find_top_k_entities(tweets, entity_desc, k):
    '''
    Find the k most frequently occuring entitites.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        k: integer

    Returns: list of entities
    '''

    lst = combine_tweets(tweets, entity_desc)
    top_k = find_top_k(lst, k)
    return top_k


# Task 2.2
def find_min_count_entities(tweets, entity_desc, min_count):
    '''
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        min_count: integer

    Returns: set of entities
    '''

    lst = combine_tweets(tweets, entity_desc)
    min_count = find_min_count(lst, min_count)
    return min_count



############## Part 3 ##############

# Pre-processing step and representing n-grams

# YOUR HELPER FUNCTIONS HERE
def pre_process(tweets, sensitive, stop_word):
    '''
    Pre-process the tweets.

    Inputs:
        tweets: a list of tweets
        sensitive: True or False
        stop_word: True or False

    Returns: a list of words after the pre-process
    '''

    word = tweets['abridged_text'].split()
    new_w = []
    for w in word:
        w = w.strip(PUNCTUATION)
        if w!="":
            if not w.startswith(STOP_PREFIXES):
                if (stop_word and w not in STOP_WORDS) or not stop_word:
                    if sensitive:
                        new_w.append(w)
                    elif not sensitive:
                        new_w.append(w.lower())
    return new_w




def n_grams(tweet_new, n):
    '''
    Change the tweet into n grams format.

    Inputs:
        tweet_new: a list of words after the pre-process
        n: integer

    Returns: a list of n grams
    '''
    lenth = len(tweet_new) - (n-1)
    if n == 1:
        tweet_new = [(tweet_new[i],) for i in range(lenth)]
    else:
        tweet_new = [tuple(tweet_new[i:(i+n)]) for i in range(lenth)]
    return tweet_new


# Task 3.1
def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n-grams.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer

    Returns: list of n-grams
    '''

    lst = []
    for tweet in tweets:
        tweet_new = pre_process(tweet, case_sensitive, stop_word=True)
        tweet_new = n_grams(tweet_new, n)
        lst.extend(tweet_new)
    top_k = find_top_k(lst, k)
    return top_k


# Task 3.2
def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer

    Returns: set of n-grams
    '''

    lst = []
    for tweet in tweets:
        tweet_new = pre_process(tweet, case_sensitive, stop_word=True)
        tweet_new = n_grams(tweet_new, n)
        lst.extend(tweet_new)
    min_count = find_min_count(lst, min_count)
    return min_count


# Task 3.3
def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Find the salient n-grams for each tweet.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        threshold: float

    Returns: list of sets of strings
    '''

    lst = []
    for tweet in tweets:
        tweet_new = pre_process(tweet, case_sensitive, stop_word=False)
        tweet_new = n_grams(tweet_new, n)
        lst.append(tweet_new)
    salient = find_salient(lst, threshold)
    return salient
