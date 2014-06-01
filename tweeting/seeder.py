from nltk.corpus import wordnet as wn
import tweet
import nltk
import gen

def synsets_seeds(word):
    seeds = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas:
            if '_' not in lemma.name: 
                seeds.add(lemma.name)
    return list(seeds)

"""
tag = "#BaylorSoftball"
statuses = tweet.api.search(tag, count=100, result_type='mixed')
print statuses
import pickle
output = open('st.pkl','wb')
pickle.dump(statuses, output)
#print twitter_seeds('#BaylorSoftball')
"""

def clean(status):
    status = list(word for word in status.split() if not word.startswith('#') \
            and len(word) > 3 and word.lower() in tweet.WORDS)
    #filter spam
    for word in status:
        if word.upper() == word and word.lower() in tweet.WORDS:
            return None
    status = list(word.lower() for word in status)
    return status

import pickle
output = open('st.pkl','rb')
statuses = pickle.load(output)
statuses = [clean(status.text) for status in statuses if not status.text.startswith('RT')]
statuses = [s for s in statuses if s]
tokens = []
for s in statuses:
    for w in s:
        tokens.append(w)

from sklearn.feature_extraction.text import TfidfVectorizer

def tokenize(text):
    return text.split()

token_dict = {
        'corpus' : gen.corpus,
        'tweets' : ' '.join(tokens)
        }
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values())
