import nltk
import sys
from nltk.util import tokenwrap

words = open('raw').read()
tokens = nltk.word_tokenize(words)
text = nltk.Text(tokens)
text.generate(15)
print tokenwrap(text._trigram_model.generate(40, sys.argv[1:]))
