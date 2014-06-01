from collections import defaultdict
import sqlite3
DB_LOC = "./db/emily_ngrams.db"

def count_unigrams(sent_list):
    unigrams = defaultdict(int)
    for sent in sent_list:
        for word in sent:
            unigrams[word] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists unigram_counts;")
        cur.execute("CREATE TABLE unigram_counts(word1 text, num int);")
        cur.executemany("insert into unigram_counts values (?, ?)", unigrams.iteritems())

def count_bigrams(sent_list):
    bigrams = defaultdict(int)
    for sent in sent_list:
        pairs = [tuple(sent[i:i+2]) for i in range(len(sent)-1)]
        for pair in pairs:
            bigrams[pair] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists bigram_counts;")
        cur.execute("create table bigram_counts(word1 text, word2 text, num int);")
        cur.executemany("insert into bigram_counts values(?,?,?)", [x+(bigrams[x],) for x in bigrams])
        
def reverse_count_bigrams(sent_list):
    bigrams = defaultdict(int)
    for sent in sent_list:
        sent = sent[:]
        sent.reverse()
        pairs = [tuple(sent[i:i+2]) for i in range(len(sent)-1)]
        for pair in pairs:
            bigrams[pair] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists reverse_bigram_counts;")
        cur.execute("create table reverse_bigram_counts(word1 text, word2 text, num int);")
        cur.executemany("insert into reverse_bigram_counts values(?,?,?)", [x+(bigrams[x],) for x in bigrams])
        
def count_trigrams(sent_list):
    trigrams = defaultdict(int)
    for sent in sent_list:
        triples = [tuple(sent[i:i+3]) for i in range(len(sent)-2)]
        for triple in triples:
            trigrams[triple] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists trigram_counts;")
        cur.execute("create table trigram_counts(word1 text, word2 text, word3 text, num int);")
        cur.executemany("insert into trigram_counts values(?,?,?, ?)", [x+(trigrams[x],) for x in trigrams])
        
def reverse_count_trigrams(sent_list):
    trigrams = defaultdict(int)
    for sent in sent_list:
        sent = sent[:]
        sent.reverse()
        triples = [tuple(sent[i:i+3]) for i in range(len(sent)-2)]
        for triple in triples:
            trigrams[triple] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists reverse_trigram_counts;")
        cur.execute("create table reverse_trigram_counts(word1 text, word2 text, word3 text, num int);")
        cur.executemany("insert into reverse_trigram_counts values(?,?,?, ?)", [x+(trigrams[x],) for x in trigrams])
        
def count_quadgrams(sent_list):
    quadgrams = defaultdict(int)
    for sent in sent_list:
        fours = [tuple(sent[i:i+4]) for i in range(len(sent)-3)]
        for four in fours:
            quadgrams[four] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists quadgram_counts;")
        cur.execute("create table quadgram_counts(word1 text, word2 text, word3 text, word4 text, num int);")
        cur.executemany("insert into quadgram_counts values(?,?,?,?,?)", [x+(quadgrams[x],) for x in quadgrams])
        
def reverse_count_quadgrams(sent_list):
    quadgrams = defaultdict(int)
    for sent in sent_list:
        sent = sent[:]
        sent.reverse()
        fours = [tuple(sent[i:i+4]) for i in range(len(sent)-3)]
        for four in fours:
            quadgrams[four] += 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists reverse_quadgram_counts;")
        cur.execute("create table reverse_quadgram_counts(word1 text, word2 text, word3 text, word4 text, num int);")
        cur.executemany("insert into reverse_quadgram_counts values(?,?,?,?,?)", [x+(quadgrams[x],) for x in quadgrams])
        
def unigram_probs():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        total = float(cur.execute("select sum(num) from unigram_counts").fetchone()[0])
        cur.execute("select * from unigram_counts;")
        counts = {}
        for v in cur:
            counts[v[0]] = v[1]/total
        cur.execute("drop table if exists unigram_probs;")
        cur.execute("create table unigram_probs (word1 text, probability float);")
        cur.executemany("insert into unigram_probs values(?,?)", counts.iteritems())

def bigram_probs():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        bigrams = {}
        cur.execute("select * from unigram_counts;")
        unigrams = {}
        for v in cur:
            unigrams[v[0]] = float(v[1])
        cur.execute("select * from bigram_counts;")
        for v in cur:
            bigrams[(v[0],v[1])] = v[2]/unigrams[v[0]]
        cur.execute("drop table if exists bigram_probs;")
        cur.execute("create table bigram_probs (word1 text, word2 text, probability float);")
        cur.executemany("insert into bigram_probs values(?,?,?)", [x+(bigrams[x],) for x in bigrams])

def reverse_bigram_probs():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        bigrams = {}
        cur.execute("select * from unigram_counts;")
        unigrams = {}
        for v in cur:
            unigrams[v[0]] = float(v[1])
        cur.execute("select * from reverse_bigram_counts;")
        for v in cur:
            bigrams[(v[0],v[1])] = v[2]/unigrams[v[0]]
        cur.execute("drop table if exists reverse_bigram_probs;")
        cur.execute("create table reverse_bigram_probs (word1 text, word2 text, probability float);")
        cur.executemany("insert into reverse_bigram_probs values(?,?,?)", [x+(bigrams[x],) for x in bigrams])
        
def trigram_probs():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        trigrams = {}
        cur.execute("select * from bigram_counts;")
        bigrams = {}
        for v in cur:
            bigrams[(v[0],v[1])] = float(v[2])
        cur.execute("select * from trigram_counts;")
        for v in cur:
            trigrams[(v[0],v[1],v[2])] = v[3]/bigrams[(v[0],v[1])]
        cur.execute("drop table if exists trigram_probs;")
        cur.execute("create table trigram_probs (word1 text, word2 text, word3 text, probability float);")
        cur.executemany("insert into trigram_probs values(?,?,?,?)", [x+(trigrams[x],) for x in trigrams])
        
def reverse_trigram_probs():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        trigrams = {}
        cur.execute("select * from reverse_bigram_counts;")
        bigrams = {}
        for v in cur:
            bigrams[(v[0],v[1])] = float(v[2])
        cur.execute("select * from reverse_trigram_counts;")
        for v in cur:
            trigrams[(v[0],v[1],v[2])] = v[3]/bigrams[(v[0],v[1])]
        cur.execute("drop table if exists reverse_trigram_probs;")
        cur.execute("create table reverse_trigram_probs (word1 text, word2 text, word3 text, probability float);")
        cur.executemany("insert into reverse_trigram_probs values(?,?,?,?)", [x+(trigrams[x],) for x in trigrams])
        
def quadgram_probs():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        quadgrams = {}
        cur.execute("select * from trigram_counts;")
        trigrams = {}
        for v in cur:
            trigrams[(v[0],v[1],v[2])] = float(v[3])
        cur.execute("select * from quadgram_counts;")
        for v in cur:
            quadgrams[(v[0],v[1],v[2],v[3])] = v[4]/trigrams[(v[0],v[1],v[2])]
        cur.execute("drop table if exists quadgram_probs;")
        cur.execute("create table quadgram_probs (word1 text, word2 text, word3 text, word4 text, probability float);")
        cur.executemany("insert into quadgram_probs values(?,?,?,?,?)", [x+(quadgrams[x],) for x in quadgrams]) 
        
def reverse_quadgram_probs():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        quadgrams = {}
        cur.execute("select * from reverse_trigram_counts;")
        trigrams = {}
        for v in cur:
            trigrams[(v[0],v[1],v[2])] = float(v[3])
        cur.execute("select * from reverse_quadgram_counts;")
        for v in cur:
            quadgrams[(v[0],v[1],v[2],v[3])] = v[4]/trigrams[(v[0],v[1],v[2])]
        cur.execute("drop table if exists reverse_quadgram_probs;")
        cur.execute("create table reverse_quadgram_probs (word1 text, word2 text, word3 text, word4 text, probability float);")
        cur.executemany("insert into reverse_quadgram_probs values(?,?,?,?,?)", [x+(quadgrams[x],) for x in quadgrams]) 
        

def sum_unigrams():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists unigrams;")
        cur.execute("create table unigrams (word1 text, probability real, summed_prob real);")
        cur.execute("select * from unigram_probs;")
        summed_probs = 0
        inserts = []
        for v in cur:
            prob = v[-1]
            summed_probs += prob
            inserts.append(v+(summed_probs,))
        cur.executemany("insert into unigrams values(?,?,?)", inserts)
        
def sum_bigrams():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists bigrams;")
        cur.execute("create table bigrams (word1 text, word2 text, probability real, summed_prob real);")
        cur.execute("select * from unigram_probs;")
        unigrams = [v[0] for v in cur]
        for unigram in unigrams:
            current = []
            cur.execute("select * from bigram_probs where word1=?;",(unigram,))
            current_sum = 0
            for bigram in cur:
                prob = bigram[-1]
                current_sum += prob
                word1 = bigram[0]
                word2 = bigram[1]
                current.append(tuple((word1, word2, prob, current_sum)))
            cur.executemany("insert into bigrams values(?,?,?,?)", current)
            
def reverse_sum_bigrams():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists reverse_bigrams;")
        cur.execute("create table reverse_bigrams (word1 text, word2 text, probability real, summed_prob real);")
        cur.execute("select * from unigram_probs;")
        unigrams = [v[0] for v in cur]
        for unigram in unigrams:
            current = []
            cur.execute("select * from reverse_bigram_probs where word1=?;",(unigram,))
            current_sum = 0
            for bigram in cur:
                prob = bigram[-1]
                current_sum += prob
                word1 = bigram[0]
                word2 = bigram[1]
                current.append(tuple((word1, word2, prob, current_sum)))
            cur.executemany("insert into reverse_bigrams values(?,?,?,?)", current)
            
def sum_trigrams():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists trigrams;")
        cur.execute("create table trigrams (word1 text, word2 text, word3 text, probability real, summed_prob real);")
        cur.execute("select * from bigram_probs;")
        bigrams = [tuple(v[:-1]) for v in cur]
        inserts = []
        for bigram in bigrams:
            current = []
            cur.execute("select * from trigram_probs where word1=? and word2=?;",(bigram))
            current_sum = 0
            for trigram in cur:
                prob = trigram[-1]
                current_sum += prob
                word1 = trigram[0]
                word2 = trigram[1]
                word3 = trigram[2]
                current.append(tuple((word1, word2, word3, prob, current_sum)))
            inserts.extend(current)
        cur.executemany("insert into trigrams values(?,?,?,?, ?)", inserts)
        
def reverse_sum_trigrams():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists reverse_trigrams;")
        cur.execute("create table reverse_trigrams (word1 text, word2 text, word3 text, probability real, summed_prob real);")
        cur.execute("select * from reverse_bigram_probs;")
        bigrams = [tuple(v[:-1]) for v in cur]
        inserts = []
        for bigram in bigrams:
            current = []
            cur.execute("select * from reverse_trigram_probs where word1=? and word2=?;",(bigram))
            current_sum = 0
            for trigram in cur:
                prob = trigram[-1]
                current_sum += prob
                word1 = trigram[0]
                word2 = trigram[1]
                word3 = trigram[2]
                current.append(tuple((word1, word2, word3, prob, current_sum)))
            inserts.extend(current)
        cur.executemany("insert into reverse_trigrams values(?,?,?,?, ?)", inserts)
        
def sum_quadgrams():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists quadgrams;")
        cur.execute("create table quadgrams (word1 text, word2 text, word3 text, word4 text, probability real, summed_prob real);")
        cur.execute("select * from trigram_probs;")
        trigrams = [tuple(v[:-1]) for v in cur]
        inserts = []
        for trigram in trigrams:
            current = []
            cur.execute("select * from quadgram_probs where word1=? and word2=? and word3=?;",(trigram))
            current_sum = 0
            for quadgram in cur:
                prob = quadgram[-1]
                current_sum += prob
                word1 = quadgram[0]
                word2 = quadgram[1]
                word3 = quadgram[2]
                word4 = quadgram[3]
                current.append(tuple((word1, word2, word3, word4, prob, current_sum)))
            inserts.extend(current)
        cur.executemany("insert into quadgrams values(?,?,?,?,?,?)", inserts)
        
def reverse_sum_quadgrams():
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        cur.execute("drop table if exists reverse_quadgrams;")
        cur.execute("create table reverse_quadgrams (word1 text, word2 text, word3 text, word4 text, probability real, summed_prob real);")
        cur.execute("select * from reverse_trigram_probs;")
        trigrams = [tuple(v[:-1]) for v in cur]
        inserts = []
        for trigram in trigrams:
            current = []
            cur.execute("select * from reverse_quadgram_probs where word1=? and word2=? and word3=?;",(trigram))
            current_sum = 0
            for quadgram in cur:
                prob = quadgram[-1]
                current_sum += prob
                word1 = quadgram[0]
                word2 = quadgram[1]
                word3 = quadgram[2]
                word4 = quadgram[3]
                current.append(tuple((word1, word2, word3, word4, prob, current_sum)))
            inserts.extend(current)
        cur.executemany("insert into reverse_quadgrams values(?,?,?,?,?,?)", inserts)
        