#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import nltk

#statefiles = nltk.corpus.state_union.fileids()

#for fileid in statefiles:
    #words = nltk.corpus.state_union.words(fileid)
    #fd = nltk.FreqDist(words)
    #print fileid, fd["men"], fd["women"], fd["people"], len(words)

fileids = nltk.corpus.state_union.fileids()
cfd = nltk.ConditionalFreqDist(
    (fileid, word)
    for fileid in fileids
    for word in nltk.corpus.state_union.words(fileid))
words = ['men', 'women', 'people']
cfd.tabulate(conditions=fileids, samples=words)
