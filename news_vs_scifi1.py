#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import division
import nltk
import codecs
from operator import itemgetter
import random



news_words = nltk.corpus.brown.words(categories='news')
scifi_words = nltk.corpus.brown.words(categories='science_fiction')

news_sents = nltk.corpus.brown.sents(categories='news')
scifi_sents = nltk.corpus.brown.sents(categories='science_fiction')

def average_length(items):
    return sum(len(i) for i in items) / len(items)

news_awl = average_length(news_words)
scifi_awl = average_length(scifi_words)
print 'awl news:', news_awl 
print 'awl scifi:', scifi_awl 

news_asl = average_length(news_sents)
scifi_asl = average_length(scifi_sents)
print 'asl news:', news_asl 
print 'asl scifi:', scifi_asl 



news_fd = nltk.FreqDist(news_words)
scifi_fd = nltk.FreqDist(scifi_words)

more_in_news = {}
more_in_scifi = {}
words = set(news_fd.keys()).union(set(scifi_fd.keys()))
len_news = len(news_words)
len_scifi = len(scifi_words)
for w in words:
    freq_news = news_fd[w] / len_news * ((len_news + len_scifi) / 2) #normalizing for length of the subcorpus
    freq_scifi = scifi_fd[w] / len_scifi * ((len_news + len_scifi) / 2)
    if freq_news > freq_scifi:
        more_in_news[w] = freq_news - freq_scifi
    elif freq_scifi > freq_news:
        more_in_scifi[w] = freq_scifi - freq_news
    
top_news = sorted(more_in_news.items(), key=itemgetter(1), reverse=True)
top_scifi = sorted(more_in_scifi.items(), key=itemgetter(1), reverse=True)

print 'NEWS'
for w, c in top_news[:100]:
    print '%s\t%d' %(w, c)
print '\n'
print 'SCIFI'
for w, c in top_scifi[:100]:
    print '%s\t%d' %(w, c)
