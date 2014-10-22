#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#this is the version I wrote at home

from __future__ import division
import nltk
import sys
import codecs

filename = sys.argv[1]
if len(sys.argv) > 2:
    n_highest = sys.argv[2]
else: n_highest = 10

text = codecs.open(filename, 'r', 'utf-8').read()
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = sent_detector.tokenize(text)
words = nltk.word_tokenize(text)
fd = nltk.FreqDist(words)

def compute_score(sent, fd):
    words = nltk.word_tokenize(sent)
    score = sum([fd[w] for w in words])
    #print sent, [fd[w] for w in words], score
    return score
    
scored_sents = [(compute_score(s, fd), s) for s in sentences]

sorted_by_score = sorted(scored_sents, reverse=True)

highest = sorted_by_score[:n_highest]

for s in scored_sents:
    if s in highest:
        print s[1]
