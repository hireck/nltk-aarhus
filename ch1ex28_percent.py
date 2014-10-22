#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import division
import nltk
from nltk.book import text5

def percent(word, text):
    fd = nltk.FreqDist(text)
    percentage = (fd[word] / len(text)) * 100
    return "%.2f%%" %(round(percentage, 2))

print percent("the", text5)
