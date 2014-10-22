#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from nltk.book import text5
        
b_sorted = sorted([w for w in text5 if w.startswith('b')])
print b_sorted
