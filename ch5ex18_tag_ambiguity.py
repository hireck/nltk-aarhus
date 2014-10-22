#18. ◑ Generate some statistics for tagged data to answer the following questions:
#a. What proportion of word types are always assigned the same part-of-speech
#tag?
#b. How many words are ambiguous, in the sense that they appear with at least
#two tags?
#c. What percentage of word tokens in the Brown Corpus involve these ambiguous
#words?

from __future__ import division
import nltk
from collections import defaultdict
from operator import itemgetter

brown = nltk.corpus.brown.tagged_words()

cfd = nltk.ConditionalFreqDist(brown)

tot_types = len(cfd)
print tot_types

#onetag = 0
#for w in cfd:
    #if len(cfd[w]) == 1:
        #onetag += 1
onetag = len([w for w in cfd if len(cfd[w])==1])        
print onetag

print onetag / tot_types * 100

ambig = [w for w in cfd if len(cfd[w])>1]
print len(ambig)

fd = nltk.FreqDist(w for (w, t) in brown)

n_ambig = sum(fd[w] for w in ambig)
print n_ambig

print n_ambig / len(brown) * 100
