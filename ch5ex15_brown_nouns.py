#15. ◑ Write programs to process the Brown Corpus and find answers to the following questions:
#a. Which nouns are more common in their plural form, rather than their singular form? (Only consider regular plurals, formed with the -s suffix.)
#b. Which word has the greatest number of distinct tags? What are they, and what do they represent?
#c. List tags in order of decreasing frequency. What do the 20 most frequent tags represent?
#d. Which tags are nouns most commonly found after? What do these tags represent?

import nltk
from collections import defaultdict
from operator import itemgetter

brown = nltk.corpus.brown.tagged_words()

tagdict = defaultdict(list)
for (w, t) in set(brown):
    tagdict[w].append(t)

lendict = {}
for w in tagdict:
    lendict[w] = len(tagdict[w])

longest = sorted(lendict.items(), key=itemgetter(1), reverse=True)
print longest[:10]
print tagdict[longest[0][0]]

tagfd = nltk.FreqDist(t for (w, t) in brown)
toptags = sorted(tagfd.items(), key=itemgetter(1), reverse=True)
print toptags[:20]

bg = nltk.bigrams(brown)


for item in bg:
    if item[1][1].startswith('NN'):
        prenoun.append(item[0][1])

fd = nltk.FreqDist(prenoun)
toptagsnoun = sorted(fd.items(), key=itemgetter(1), reverse=True)
print toptagsnoun[:20]
