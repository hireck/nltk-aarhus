#17. ◑ What is the upper limit of performance for a lookup tagger, assuming no limit
#to the size of its table? (Hint: write a program to work out what percentage of tokens
#of a word are assigned the most likely tag for that word, on average.)

from __future__ import division
import nltk
from collections import defaultdict
from operator import itemgetter

brown = nltk.corpus.brown.tagged_words()

cfd = nltk.ConditionalFreqDist(brown)

correct = 0

for w in cfd:
    toptag = cfd[w].max()
    n = cfd[w][toptag]
    correct += n
    
print correct / len(brown)
