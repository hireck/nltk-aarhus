#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import nltk
import codecs
import xml.etree.ElementTree as ET
from collections import defaultdict

xml = ET.parse('/media/data/lectures_aarhus/nltk_python/Parole/parole-dk.tei.utf8.xml')

lemmas = defaultdict(list)

for w in xml.iter('W'):
    form = w.text
    tag = w.get('msd')
    lemma = w.get('lemma')
    lemmas['/'.join([form, tag])].append(lemma)

lemmas_out = {}    
for i in lemmas:
    if len(set(lemmas[i])) == 1:
        lemmas_out[i] = lemmas[i][0]
    else:
        print i, lemmas[i]

lemmas_out[u'løjet/VAPA=S[CN]I[ARU]-U'] = u'løje'
lemmas_out[u'Camilo/NP--U==-'] = u'Camilo'
lemmas_out[u'dvs./RGU'] = u'det_vil_sige'
lemmas_out[u'enkelt/ANP---=-R'] = u'enkel'
lemmas_out[u'TV-Avisen/NCCSU==D'] = u'TV-Avis'
lemmas_out[u'Danmarks-serien/NCCSU==D'] = u'Danmarks-serie'
lemmas_out[u'Cup/NCCSU==I'] = u'cup'
lemmas_out[u'ja-stemmer/NCCPU==I'] = u'ja-stemme'
lemmas_out["CD'er/NCCPU==I"] = u'CD'
lemmas_out[u'Cotton/NP--U==-'] = u'Cotton'
lemmas_out[u'Gøngehøvdingen/NCCSU==D'] = u'gøngehøvding'
lemmas_out[u'misforhold/NCNSU==I'] = u'misforhold'
lemmas_out[u'studier/NCNPU==I'] = u'studie'
lemmas_out[u'tusinder/NCNPU==I'] = u'tusind'
lemmas_out[u'arbejder-/XX'] = u'arbejder-'
lemmas_out[u'TVs/NCNSG==I'] = u'TV'
lemmas_out[u'Bosnien-Hercegovina/NP--U==-'] = u'Bosnien-Hercegovina'
lemmas_out[u'TV-Avis/NCCSU==I'] = u'TV-Avis'
lemmas_out[u'P-pillerne/NCCPU==D'] = u'P-pille'
lemmas_out[u'Europa-Parlamentet/NCNSU==D'] = u'Europa-Parlament'
lemmas_out[u'køer/NCCPU==I'] = u'køer' #ko, kø
lemmas_out[u'Danfoss-lærlinge/NCCPU==I'] = u'Danfoss-lærling'
lemmas_out[u'banker/NCCPU==I'] = u'bank'
lemmas_out[u'cand._jur./XA'] = u'candidatus_juris'
lemmas_out[u'tanken/NCCSU==D'] = u'tanke'
lemmas_out[u'givet/ANP[CN]SU=IU'] = u'givet'
lemmas_out[u'A-kasserne/NCCPU==D'] = u'A-kasse'
lemmas_out[u'stk./NCNSU==I'] = u'styk'
lemmas_out[u'3./AO---U=--'] = u'3'
lemmas_out[u'America/NP--U==-'] = u'America'
lemmas_out[u'cand._psych./XA'] = u'candidatus_psychologiae'


            
outfile = codecs.open('parole_lemmas.txt', 'w', 'utf-8')
for k in sorted(lemmas_out.keys()):
    outfile.write('\t'.join([k, lemmas_out[k]+'\n']))
outfile.close()
