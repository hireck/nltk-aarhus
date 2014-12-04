#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import division
import nltk
from operator import itemgetter
from collections import defaultdict
import codecs
import pickle
import os
from math import sqrt
import xml.etree.ElementTree as etree
from nltk.corpus.reader.tagged import CategorizedTaggedCorpusReader
from gensim.models import Word2Vec
import logging

categories = pickle.load(open('parole_categories.pickle', 'r'))
parole = CategorizedTaggedCorpusReader('parole_nltk', '.*', cat_map=categories)

preps = [w.lower() for (w, t) in parole.tagged_words() if t == 'SP']
preps_fd = nltk.FreqDist(preps)
main_preps = [p for p in preps_fd.keys() if preps_fd[p] > 10]

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = parole.sents()
print sentences[0]

model = Word2Vec(sentences, min_count=5)

for p in main_preps:
    print p, model.most_similar(positive=[p], topn=5)
