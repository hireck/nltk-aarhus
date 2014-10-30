#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import nltk
from operator import itemgetter
import codecs

corpus_root = '/media/data/lectures_aarhus/nltk_python/Parole'
fileid = 'parole-dk.tei.utf8.xml'
parole = nltk.corpus.XMLCorpusReader(corpus_root, [fileid])

xml = parole.xml()

tagged_sents = []
tagged_words = []

sents = xml.iter('s')
for s in sents:
    words = s.findall('W')
    tagged = []
    for w in words:
        form = w.text
        tag = w.get('msd')
        lemma = w.get('lemma')
        tagged.append((form, tag, lemma))
    tagged_sents.append(tagged)
    tagged_words.extend(tagged)
    
preps = [l for (w, t, l) in tagged_words if t == 'SP']

preps_fd = nltk.FreqDist(preps)
sorted_preps = sorted(preps_fd.items(), key=itemgetter(1), reverse=True) 
outfile = codecs.open('sorted_preps.txt', 'w', 'utf-8')
outfile.write(', '.join(['%s:%d'%(l,c) for (l, c) in sorted_preps]))

print len(tagged_words)
print len(tagged_sents)
