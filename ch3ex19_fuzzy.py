#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import division
import nltk

lines = open('fuzzy.txt').readlines()

items = []
for l in lines:
	w, n = l.split()
	items.append([w, int(n)])
	
print items
