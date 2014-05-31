from collections import defaultdict
import sqlite3
DB_LOC = "/Users/benicorp/Dropbox/EmilyTweets/db/emily_ngrams.db"

def count_unigrams(poem_list):
    unigrams = defaultdict(int)
    for poem in poem_list:
        starts = ["back3", "back2", "back1"]
        starts.extend(poem)
        for word in starts:
            unigrams[word] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists unigrams;")
        cur.execute("CREATE TABLE unigrams(word1 text, num int);")
        cur.executemany("insert into unigrams values (?, ?)", unigrams.iteritems())

def count_bigrams(poem_list):
    bigrams = defaultdict(int)
    for poem in poem_list:
        starts = ["back3", "back2", "back1"]
        starts.extend(poem)
        pairs = [tuple(starts[i:i+2]) for i in range(len(starts)-1)]
        for pair in pairs:
            bigrams[pair] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists bigrams;")
        cur.execute("create table bigrams(word1 text, word2 text, num int);")
        cur.executemany("insert into bigrams values(?,?,?)", [x+(bigrams[x],) for x in bigrams])
        
def count_trigrams(poem_list):
    trigrams = defaultdict(int)
    for poem in poem_list:
        starts = ["back3", "back2", "back1"]
        starts.extend(poem)
        triples = [tuple(starts[i:i+3]) for i in range(len(starts)-2)]
        for triple in triples:
            trigrams[triple] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists trigrams;")
        cur.execute("create table trigrams(word1 text, word2 text, word3 text, num int);")
        cur.executemany("insert into trigrams values(?,?,?, ?)", [x+(trigrams[x],) for x in trigrams])
        
def count_quadgrams(poem_list):
    quadgrams = defaultdict(int)
    for poem in poem_list:
        starts = ["back3", "back2", "back1"]
        starts.extend(poem)
        fours = [tuple(starts[i:i+4]) for i in range(len(starts)-3)]
        for four in fours:
            quadgrams[four] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists quadgrams;")
        cur.execute("create table quadgrams(word1 text, word2 text, word3 text, word4 text, num int);")
        cur.executemany("insert into quadgrams values(?,?,?,?,?)", [x+(quadgrams[x],) for x in quadgrams])