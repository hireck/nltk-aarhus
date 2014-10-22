#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import division
import nltk
import codecs
from operator import itemgetter

text = codecs.open('Hvor_er_Bo.txt', "r", "utf-8").read() #reading in the file
print text[:100] #printing the first 100 characters

words = nltk.word_tokenize(text) #tokenizing
print words[:10] #printing the first 10 words

# now we'll make a frequency distribution:
fd = nltk.FreqDist([w.lower() for w in words]) #lowercasing everything, so 'The' is counted as an instance of 'the'
vocab = sorted(fd.items(), key=itemgetter(1), reverse=True) #sorting the vocabulary by decreasing frequency
outfile = codecs.open('bo_freqs.txt', "w", "utf-8") #opening(creating) a file to write to
for (word, freq) in vocab[:100]: #looping over the first 100 items
    output = '%s\t%s\n' %(word, freq) #formatting for writing: \t is a tab, \n is a new line
    outfile.write(output) #writing the formatted string to the output file
outfile.close() #closing the output file

# lets try a sentence tokenizer
sent_detector = nltk.data.load('tokenizers/punkt/danish.pickle') #loading the pre-built tokenizer
sents = sent_detector.tokenize(text) #running it on the text
print sents[:3] #printing the first 3 sentences

#It doesn't work great. The sentence break after a chapter heading is not detected, because there is no period, even though there are 2 line breaks and a capital letter:

#Bo vil i kiosken
#
#Det er søndag morgen.

#now with an nltk corpus
#I downloaded the Dutch Alpino corpus with nltk.download() and then selecting it in the corpora tab

alp = nltk.corpus.alpino.words() #loading the words of the corpus
fd_alp = nltk.FreqDist([w.lower() for w in alp])
vocab_alp = sorted(fd_alp.items(), key=itemgetter(1), reverse=True) 
outfile2 = codecs.open('alp_freqs.txt', "w", "utf-8") 
for (word, freq) in vocab_alp[:100]: 
    output = '%s\t%s\n' %(word, freq) 
    outfile2.write(output) 
outfile2.close() 


#I've repeated a lot of code here, so let's write a function:

def fd_to_file(words, filename, n):
    '''makes a frequency distribution and writes the first n items to a file'''
    fd = nltk.FreqDist([w.lower() for w in words])
    vocab = sorted(fd.items(), key=itemgetter(1), reverse=True)
    outfile = codecs.open(filename, "w", "utf-8")
    for (word, freq) in vocab[:n]:
        output = '%s\t%s\n' %(word, freq) 
        outfile.write(output) 
    outfile.close() 
    
#we can use it like this:    
    
text = codecs.open('Hvor_er_Bo.txt', "r", "utf-8").read()
tokens = nltk.word_tokenize(text)
fd_to_file(tokens, 'bo_freqs2.txt', 100)

fd_to_file(nltk.corpus.alpino.words(), 'alp_freqs2.txt', 100)
