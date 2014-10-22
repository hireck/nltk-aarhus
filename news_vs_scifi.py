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
    

#Traning a Classifier 

files = ([(fid, 'news') for fid in nltk.corpus.brown.fileids(categories='news')] + [(fid, 'scifi') for fid in nltk.corpus.brown.fileids(categories='science_fiction')])
random.shuffle(files)

print files

size = int(len(files) * 0.5)
train_files = files[:size]
#test_files = files[size:]

allwords = [] 
for (fid, cat) in train_files:
    allwords.extend(nltk.corpus.brown.words(fileids=fid))
fd = nltk.FreqDist(allwords)
top_words = sorted(fd.items(), key=itemgetter(1), reverse=True)[:500]
word_features = [w for (w, f) in top_words]
#print word_features

def genre_features(f):
    f_words = nltk.corpus.brown.words(fileids=f)
    fd = nltk.FreqDist(f_words)
    top_words = [w for (w, f) in sorted(fd.items(), key=itemgetter(1), reverse=True)[:500]]
    features = {}
    for w in word_features:
        features['contains(%s)' % w] = (w in top_words)
    return features

featuresets = [(genre_features(fid), cat) for (fid, cat) in files]
train_set = featuresets[:size]
test_set = featuresets[size:]

nb_classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(nb_classifier, test_set)
print nb_classifier.show_most_informative_features(5)
    
