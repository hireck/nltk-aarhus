#30. ◑ Preprocess the Brown News data by replacing low-frequency words with UNK,
#but leaving the tags untouched. Now train and evaluate a bigram tagger on this
#data. How much does this help? What is the contribution of the unigram tagger
#and default tagger now?

import nltk
from collections import defaultdict

news = nltk.corpus.brown.tagged_words(categories='news')
vocab = nltk.FreqDist(w for (w, t) in news)
topvocab = [w for w in vocab if vocab[w] > 1]

mapping = defaultdict(lambda: 'UNK')
for v in topvocab:
    mapping[v] = v
    
news2 = [mapping[v] for v in news]

news2 = nltk.corpus.brown.tagged_sents(categories="news")

sents = []
for s in news2:
    sents.append([(mapping[w], t) for (w, t) in s])

print sents[:2]

size = int(len(sents) * 0.9)
train_sents = sents[:size]
test_sents = sents[size:]

t0 = nltk.DefaultTagger('NN')
t1 = nltk.UnigramTagger(train_sents, backoff=t0)
t2 = nltk.BigramTagger(train_sents, backoff=t1)

print t2.evaluate(test_sents)

t3 = nltk.BigramTagger(train_sents)
print t3.evaluate(test_sents)
