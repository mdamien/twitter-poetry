import sqlite3
from math import log

google_unigram_loc = "./db/google_unigrams.db"
emily_db_loc = "./db/emily_ngrams.db"
total_google_unigrams = 6057866345.0

def tfidf_emily(word):
    word_idf = idf(word)
    with sqlite3.connect(emily_db_loc) as con:
        cur = con.cursor()
        cur.execute("select num from unigram_counts where word1=?", (word,))
        freq = list(cur)
        if freq:
            freq=freq[0][0]
        else:
            freq = 0
    return freq*word_idf
    
def tfidf_tags(tag, tag_count, total):
    word_idf = idf(word)
    return (tag_count/total)*word_idf

def idf(word):
    with sqlite3.connect(google_unigram_loc) as con:
        cur = con.cursor()
        cur.execute("select count from google_unigrams where word=?", (word,))
        count = list(cur)
        if count:
            count = count[0][0]
        else:
            count = 2
    return log(count/total_google_unigrams, 2)