#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import nltk
from operator import itemgetter
import codecs

lines = codecs.open('creole_test.txt', "r", "utf-8").readlines() # reading the file as a list of lines

wordlines = [l.split()[1:] for l in lines if l.startswith('\mb')] 
#extracting the lines with the normalized words
#already splitting them into a list of words, and removing the \mb prefix (the zeroth element)
taglines = [l.split()[1:] for l in lines if l.startswith('\ps')] #same for the tags

linepairs = zip(wordlines, taglines) 
#combining word lines and tag lines into pairs that belong together
#if there are inconsistencies in the input file, that may lead to trouble here, 
#in that case, make sure that each sentence has a line of tags and that all the prefixes are correct

tagged_sents = [zip(words, tags) for words, tags in linepairs]
#now each sentence is a list of pairs(tuples of lenght 2): [(word1, tag1), (word2, tag2), ...]

print tagged_sents[0]
#checking if the results looks ok

#if you create a file that has the same format as the brown corpus tagged files, 
#you should be able to load it in the same way and perform the same operations
#should be somehting like this, but I haven't checked the details yet
outfile = codecs.open('creole_tagged.txt', "w", "utf-8") 
for s in tagged_sents:
    brown_style = ['/'.join([w, t]) for (w, t) in s]
    outfile.write((' '.join(brown_style))+'\n')
