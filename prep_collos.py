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

def get_collos(context_fd, words_fd, tot_words):
    threshold = sqrt(12.12 / tot_words) #significance threshold for phi (p < 0.0005)
    #print threshold
    collos = defaultdict(list)
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
#main program starts here

#loading the data form the xml file
xml = ET.parse('/media/data/lectures_aarhus/nltk_python/Parole/parole-dk.tei.utf8.xml')

tagged_sents = [] #we're going to collect all sentences
tagged_words = [] #and all words

sents = xml.iter('s') #extracting all sentences for the xml
for s in sents:
    words = s.findall('W') #extracting all words from the sentence
    tagged = [] # here we collect all the words in the sentence, with their tags and lemmas
    for w in words:
        form = w.text #the wordform is written as text in the W element
        tag = w.get('msd') #get the tag if the word
        lemma = w.get('lemma') #get the lemma of the word
        tagged.append((form, tag, lemma)) #make a 3-place tuple 
    tagged_sents.append(tagged) #add as a list to sentences
    tagged_words.extend(tagged) #add the single items to words

#listing the prepostions (by lemma)    
preps = [l for (w, t, l) in tagged_words if t == 'SP'] 

preps_fd = nltk.FreqDist(preps) #making a freqdist over prepostions
sorted_preps = sorted(preps_fd.items(), key=itemgetter(1), reverse=True) 
main_preps = [p for p in preps_fd.keys() if preps_fd[p] > 10] 
#selecting prepostions that occur more than 10 times
print main_preps

tot_words = len(tagged_words) #the total number of words in the corpus
lemmas = [l for (w, t, l) in tagged_words] #getting a list of only lemmas
#words_fd = nltk.FreqDist(tagged_words)
words_fd = nltk.FreqDist(lemmas) #making a freqdist over lemmas

#setting up some infrastructure for counting left and right context words for each preposition:
left_context_fd = {}
right_context_fd = {}
for p in main_preps:
    left_context_fd[p] = defaultdict(int)
    right_context_fd[p] = defaultdict(int)

bigrams = []
for s in tagged_sents:
    bigrams.extend(nltk.ngrams(s, 2)) #or: bigrams.extend(nltk.bigrams(s))
    
for bg in bigrams:
    wtl1, wtl2 = bg[0], bg[1]
    w1, t1, l1 = wtl1
    w2, t2, l2 = wtl2
    if l1 in main_preps:
        right_context_fd[l1][l2] += 1
    if l2 in main_preps:
        left_context_fd[l2][l1] += 1


left_collos = get_collos(left_context_fd, words_fd, tot_words)
right_collos = get_collos(right_context_fd, words_fd, tot_words)

for p in main_preps:
    topleft = ['%s(%.2f)'%(word, score) for (word, score) in sorted(left_collos[p], key=itemgetter(1), reverse=True)[:10]]
    print p.upper(), ', '.join(topleft)
print '\n'    
for p in main_preps:
    topright = ['%s(%.2f)'%(word, score) for (word, score) in sorted(right_collos[p], key=itemgetter(1), reverse=True)[:10]]
    print p.upper(), ', '.join(topright)
