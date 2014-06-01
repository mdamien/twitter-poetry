import sqlite3, random
from preprocess import end_sent
DB_LOC = "/Users/benicorp/Dropbox/EmilyTweets/db/emily_ngrams.db"

def choose_word_ahead(prev1, prev2, prev3=None):
    choose = random.random()
    with sqlite3.connect(DB_LOC) as con:
        cur=con.cursor()
        res = ''
        if prev3:
            try:
                cur.execute("select word4 from quadgrams where word1=? and word2=? and word3=? and summed_prob>=? order by summed_prob asc limit 1;", (prev1, prev2, prev3, choose))
                res = cur.fetchone()[0]
            except TypeError:
               pass
        if not res:
            try:
                cur.execute("select word3 from trigrams where word1=? and word2=? and summed_prob>=? order by summed_prob asc limit 1;", (prev1, prev2, choose))
                res = cur.fetchone()[0]
            except TypeError:
                 cur.execute("select word2 from bigrams where word1=? and summed_prob>=? order by summed_prob asc limit 1;", (prev2, choose))
                 res = cur.fetchone()[0]
    return res
    
def choose_word_back(next1, next2, next3=None):
    choose = random.random()
    with sqlite3.connect(DB_LOC) as con:
        cur=con.cursor()
        res = ''
        if next3:
            try:
                cur.execute("select word1 from quadgrams where word2=? and word3=? and word4=? and summed_prob>=? order by summed_prob asc limit 1;", (next1, next2, next3, choose))
                res = cur.fetchone()[0]
            except TypeError:
               pass
        if not res:
            try:
                cur.execute("select word1 from trigrams where word2=? and word3=? and summed_prob>=? order by summed_prob asc limit 1;", (next1, next2, choose))
                res = cur.fetchone()[0]
            except TypeError:
                 cur.execute("select word1 from bigrams where word2=? and summed_prob>=? order by summed_prob asc limit 1;", (next1, choose))
                 res = cur.fetchone()[0]
    return res
    
def trigrams_forward(seed_word, randomize=True):
    sent = []
    word1 = ''
    word2 = ''
    word3 = ''
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        if randomize:
            cur.execute("select * from trigrams where word1=?", (seed_word,))
            choose = random.random()
            current = cur.next()
            try:
                while current[-1] <= choose:
                    current = cur.next()
            except StopIteration:
                pass
        else:
            cur.execute("select * from trigrams where word1=? order by probability desc limit 1;", (seed_word,))
            current = cur.next()
        word1 = current[0]
        word2 = current[1]
        word3 = current[2]
        sent.append(word1)
        sent.append(word2)
        sent.append(word3)
        word1, word2 = word2, word3
        while word3 not in end_sent:
            word3 = choose_word_ahead(word1, word2)
            sent.append(word3)
            word1, word2 = word2, word3
    return sent
    
def trigrams_back(seed_word, randomize=True):
    sent = []
    word1 = ''
    word2 = ''
    word3 = ''
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        if randomize:
            cur.execute("select * from trigrams where word3=?", (seed_word,))
            choose = random.random()
            current = cur.next()
            try:
                while current[-1] <= choose:
                    current = cur.next()
            except StopIteration:
                pass
        else:
            cur.execute("select * from trigrams where word3=? order by probability desc limit 1;", (seed_word,))
            current = cur.next()
        word3 = current[2]
        sent.insert(0, word3)
        word2 = current[1]
        sent.insert(0, word2)
        word1 = current[0]
        sent.insert(0, word1)
        word2, word3 = word1, word2
        done = False
        while not done:
            word1 = choose_word_back(word2, word3)
            if not word1[-1].isdigit():
                sent.insert(0, word1)
                word2, word3 = word1, word2
            else:
                done = True
    return sent
    
def quadgrams_forward(seed_word, randomize=True):
    sent = []
    word1 = ''
    word2 = ''
    word3 = ''
    word4 = ''
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        if randomize:
            cur.execute("select * from quadgrams where word1=?", (seed_word,))
            choose = random.random()
            current = cur.next()
            try:
                while current[-1] <= choose:
                    current = cur.next()
            except StopIteration:
                pass
        else:
            cur.execute("select * from quadgrams where word1=? order by probability desc limit 1;", (seed_word,))
            current = cur.next()
        word1 = current[0]
        word2 = current[1]
        word3 = current[2]
        word4 = current[3]
        sent.append(word1)
        sent.append(word2)
        sent.append(word3)
        sent.append(word4)
        while word4 not in end_sent:
            word4 = choose_word_ahead(word1, word2, word3)
            sent.append(word4)
            word1, word2, word3 = word2, word3, word4
    return sent
    
def quadgrams_back(seed_word, randomize=True):
    sent = []
    word1 = ''
    word2 = ''
    word3 = ''
    word4 = ''
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        if randomize:
            cur.execute("select * from quadgrams where word4=?", (seed_word,))
            choose = random.random()
            current = cur.next()
            try:
                while current[-1] <= choose:
                    current = cur.next()
            except StopIteration:
                pass
        else:
            cur.execute("select * from quadgrams where word1=? order by probability desc limit 1;", (seed_word,))
            current = cur.next()
        word1 = current[0]
        word2 = current[1]
        word3 = current[2]
        word4 = current[3]
        sent.append(word1)
        sent.append(word2)
        sent.append(word3)
        sent.append(word4)
        done = False
        while not done:
            word1 = choose_word_back(word2, word3, word4)
            if not word1[-1].isdigit():
                sent.insert(0, word1)
                word2, word3, word4 = word1, word2, word3
            else:
                done = True
    return sent
    

    