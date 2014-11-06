#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import nltk
from operator import itemgetter
import codecs
import pickle
import os
import xml.etree.ElementTree as etree
from nltk.corpus.reader.tagged import CategorizedTaggedCorpusReader

#corpus_root = '/media/data/lectures_aarhus/nltk_python/Parole'
#fileid = 'parole-dk.tei.utf8.xml'
#parole = nltk.corpus.XMLCorpusReader(corpus_root, [fileid])

xml = etree.parse('/media/data/lectures_aarhus/nltk_python/Parole/parole-dk.tei.utf8.xml')

catcodes = {}
cats = xml.iter('category')
for c in cats:
    idf = c.get('ID')
    desc = c.find('catDesc').text
    catcodes[idf] = desc
    
categories = {}

teis = xml.iter('tei.2')
for tei in teis:
    codes = []
    catrefs = tei.iter('catRef')
    for c in catrefs:
        codes.append(c.get('target'))
    text = tei.find('text')
    idf = text.get('id')
    categories[idf] = [catcodes[c] for c in codes]
    sents = text.iter('s')
    tagged_sents = []
    for s in sents:
        words = s.findall('W')
        tagged = []
        for w in words:
            form = w.text
            tag = w.get('msd')
            #lemma = w.get('lemma')
            tagged.append('/'.join([form, tag]))
        tagged_sents.append(' '.join(tagged))
        write_sents = ['\t'+s for s in tagged_sents]
    outfile = codecs.open(os.path.join('parole_nltk', idf), 'w', 'utf-8')
    outfile.write('\n\n'.join(write_sents))

#pickle.dump(categories, open('parole_nltk/categories.pickle', 'w'))
pickle.dump(categories, open('parole_categories.pickle', 'w'))


#>>> import nltk
#>>> import pickle
#>>> categories = pickle.load(open('parole_categories.pickle', 'r'))
#>>> from nltk.corpus.reader.tagged import CategorizedTaggedCorpusReader
#>>> parole = CategorizedTaggedCorpusReader('parole_nltk', '.*', cat_map=categories)
#>>> parole.words()
#[u'To', u'kendte', u'russiske', u'historikere', ...]
#>>> parole.categories()
#["'names'", 'Account, minutes', 'Article', 'Background article', 'Causerie', 'Column', 'Consumer advice', 'Debate', 'EU', 'Editorial', 'Editorial matters', 'Essay', 'Feature article', 'Information booklet', 'Information leaflet', 'Interview', 'Letter to the editor', 'Message', 'N/A', 'News article', 'News broadcast', 'Notice', 'On-the-spot report', 'Programme', 'Review', 'Small news item', 'advertising', 'agriculture', 'announcement', 'anthropology', 'aphorism', 'architecture', 'art', 'astronomy', 'autobiography', 'biography', 'biograpical', 'biology', 'book', 'botany', 'business', 'chemistry', 'clothing', 'communication', 'computer science', 'construction', 'consumer items', 'corr. column questions', 'correspondence column', 'crafts', 'crime', 'culture', 'diary', 'economics', 'electronic', 'environment', 'ephemera', 'fairy tale', 'family', 'film', 'fishing and hunting', 'food', 'games', 'general science/scholarship', 'geography', 'handbook', 'health', 'history', 'horoscope', 'housing', 'how-to guide', 'industry', 'journal', 'languages', 'law', 'law text', 'leisure', 'library sciences', 'literature', 'local', 'magazine', 'mathematics', 'military', 'monograph', 'music and dance', 'natural sciences', 'newspaper', 'novel', 'obituary', 'pedagogics', 'photography', 'physics', 'politics', 'press', 'prior publicity', 'private letter', 'profile', 'psychology', 'radio', 'reference book', 'religion', 'school textbook', 'series (tv)', 'sermon', 'sex/living together', 'short story', 'social services', 'society/social studies', 'specialized journal/magazine', 'sport', 'story', 'student essay', 'teaching/education', 'technology', 'television', 'textbook', 'theatre', 'trade', 'traffic', 'transportation', 'travel', 'travel book', 'work of reference', 'zoology']
