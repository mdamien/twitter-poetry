import nltk
import sys
from nltk.util import tokenwrap

corpus = open('db/data').read()

tokens = nltk.word_tokenize(corpus)
text = nltk.Text(tokens)
text.generate(0) #generate model

LIMIT = 140

def gen(context='', hashtag='', tries=30):
    n = 10
    r = tokenwrap(text._trigram_model.generate(n, context))
    return r[:140-len(hashtag)]+' '+hashtag

if __name__ == '__main__':
    print gen(sys.argv[2:], sys.argv[1])
