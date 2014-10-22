#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import nltk
from nltk.book import text5

fd = nltk.FreqDist([w for w in text5 if len(w)==4])

print fd
