import sqlite3
from math import log

google_unigram_loc = "./db/google_unigrams.db"
emily_db_loc = "./db/emily_ngrams.db"
idf_db_loc = "./db/idf.db"
total_google_unigrams = 6057866345.0

from nltk.corpus import stopwords as sw
stopwords = set(sw.words())

def tfidf_emily(word):
    if word in stopwords:
        return 0
    word_idf = get_idf(word)
    with sqlite3.connect(emily_db_loc) as con:
        cur = con.cursor()
        cur.execute("select num from unigram_counts where word1=?", (word,))
        freq = list(cur)
        if freq:
            freq=freq[0][0]
        else:
            freq = 0
    return freq*word_idf
    
def tf_tag(tag, tag_count, total):
    return float(tag_count)/total
    
# def tfidf_tags(tag, tag_count, total):
#     if word in stopwords:
#         return 0
#     return tf_tag(tag, tag_count, total)*word_idf

def get_idf(word):
    if word in stopwords:
        return 0
    with sqlite3.connect(google_unigram_loc) as con:
        cur = con.cursor()
        cur.execute("select count from google_unigrams where word=?", (word,))
        count = list(cur)
        if count:
            count = count[0][0]
        else:
            count = 2
    return 1.0/log(count/total_google_unigrams, 2)