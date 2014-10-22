#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from nltk.book import text6

for w in text6:
    if w.isupper():
        print w
        
ize_words = [w for w in text6 if w.endswith('ize')]
print ize_words

z_words = [w for w in text6 if 'z' in w]
print z_words

pt_words = [w for w in text6 if 'pt' in w]
print pt_words

#lower_words = [w for w in text6 if (w.islower() or w.istitle())]
#print lower_words
