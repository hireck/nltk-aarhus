#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import division
import nltk
import codecs
import pickle
import os
from operator import itemgetter
from collections import defaultdict
from math import sqrt
import xml.etree.ElementTree as ET
from nltk.corpus.reader.tagged import CategorizedTaggedCorpusReader

#*****************************************************
#FUNCTIONS

def smooth(count): #adjust counts so as to not pay too much attention to rare terms (absolute discounting)
    return count - 1

def phi(count, fw1, fw2, tot):
    '''compute association strength between two items, 
    based on their cooccurrence count, the frequnecy of each of them and the total number of items'''
    obs_w1_w2 = count
    obs_w1_notw2 = fw1 - count
    obs_notw1_w2 = fw2 - count
    notw1 = tot - fw1
    notw2 = tot - fw2
    obs_notw1_notw2 = notw1 - obs_notw1_w2
    exp_w1_w2 = fw1 * fw2 / tot
    exp_w1_notw2 = fw1 * notw2 / tot
    exp_notw1_w2 = notw1 * fw2 / tot
    exp_notw1_notw2 = notw1 * notw2 / tot
    diff_w1_w2 = (obs_w1_w2 - exp_w1_w2)**2 / exp_w1_w2
    diff_w1_notw2 = (obs_w1_notw2 - exp_w1_notw2)**2 / exp_w1_notw2
    diff_notw1_w2 = (obs_notw1_w2 - exp_notw1_w2)**2 / exp_notw1_w2
    diff_notw1_notw2 = (obs_notw1_notw2 - exp_notw1_notw2)**2 / exp_notw1_notw2
    chisquare = diff_w1_w2 + diff_w1_notw2 + diff_notw1_w2 + diff_notw1_notw2
    phi = sqrt(chisquare / tot)
    return phi

def get_assoc_words(words_fd, cat_words_fd, cat_tot, tot_words):
    threshold = sqrt(12.12 / tot_words) #significance threshold for phi (p < 0.0005)
    #print threshold
    assocs = defaultdict(list)
    for prep in context_fd:
        collocations = {}
        for w in context_fd[prep]:
            smoothcount = smooth(context_fd[prep][w])
            if smoothcount > words_fd[prep] * words_fd[w] / tot_words:
                score = phi(smoothcount, words_fd[prep], words_fd[w], tot_words)
                if score > threshold:
                    collos[prep].append((w, round(score, 2))) 
    return collos

#****************************************************************

categories = pickle.load(open('parole_categories.pickle', 'r'))
parole = CategorizedTaggedCorpusReader('parole_nltk', '.*', cat_map=categories)

tot_words = len(parole.words())
words_fd = nltk.FreqDist(parole.words())

cats_words_df = {}
cats_tots = {}
for cat in parole.categories():
    words = parole.words(categories=cat)
    cats_words_df[cat] = nltk.FreqDist(words)
    cats_tots[cat] = len(words)
    
for cat in parole.categories():
    print cat, cats_tots[cat]
    
assocs = defaultdict(list)   
for cat in parole.categories():
    threshold = sqrt(12.12 / tot_words)
    for w in cats_words_df[cat]:
        smoothcount = smooth(cats_words_df[cat][w])
        if smoothcount > words_fd[w] * cats_tots[cat] / tot_words:
            score = phi(smoothcount, words_fd[w], cats_tots[cat], tot_words)
            if score > threshold:
                assocs[cat].append((w, round(score, 2)))
                
for c in parole.categories():
    top = ['%s(%.2f)'%(word, score) for (word, score) in sorted(assocs[c], key=itemgetter(1), reverse=True)[:10]]
    print c.upper(), ', '.join(top)
