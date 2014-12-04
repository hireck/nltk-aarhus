#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import division
import nltk
import codecs
from operator import itemgetter
import random

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
    
for fid, cat in files[size:]:
    prediction = nb_classifier.classify(genre_features(fid))
    if not prediction == cat:
        print fid, prediction, cat
        
truth = [cat for (fid, cat) in files[size:]]
predictions = [nb_classifier.classify(genre_features(fid)) for (fid, cat) in files[size:]]

print nltk.ConfusionMatrix(truth, predictions)
