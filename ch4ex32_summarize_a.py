#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''Develop a simple extractive summarization tool, that prints the sentences of a document which contain 
the highest total word frequency. Use FreqDist() to count word frequencies, 
and use sum to sum the frequencies of the words in each sentence. 
Rank the sentences according to their score. 
Finally, print the n highest-scoring sentences in document order. 
Carefully review the design of your program, especially your approach to this double sorting. 
Make sure the program is written as clearly as possible. '''

from __future__ import division
import nltk
import sys
import codecs

filename = sys.argv[1]
if len(sys.argv) > 2:
    n_highest = int(sys.argv[2])
else: n_highest = 10

text = codecs.open(filename, encoding='utf-8').read()
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
sents = sent_detector.tokenize(text)
#print sents[:2]

words = nltk.word_tokenize(text)
fd = nltk.FreqDist(words)

# tokenized_sents = [nltk.word_tokenize(s) for s in sents]
# print tokenized_sents[:2]

sums = []
for s in sents:
	tokens = nltk.word_tokenize(s)
	tot = sum([fd[w] for w in tokens])
	sums.append((tot, s))
	
topsents = sorted(sums, reverse=True)[:n_highest]
selection = [s for (n, s) in topsents]

for s in sents:
	if s in selection:
		print s
