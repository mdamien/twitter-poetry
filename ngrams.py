from collections import defaultdict
import sqlite3
DB_LOC = "~Dropbox/EmilyTweets/db/emily_ngrams.db"

def count_unigrams(poem_lists):
    unigrams = defaultdict(int)
    for poem in poem_list:
        starts = ["back3", "back2", "back1"]
        poem = starts.extend(poem)
        for word in poem:
            unigrams[word] += 1
    
    con = sqlite3.connect(DB_LOC)
    cur = con.cursor()
    cur.execute("drop table if exists unigrams;")
    cur.execute("CREATE TABLE unigrams(word1 text, count int, probability real, sum_probs real;")
    cur.executemany(