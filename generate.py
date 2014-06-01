import sqlite3, random
from operator import itemgetter
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
    
def combined_forward(seed_word, randomize=True):
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
        prev_word1 = word1
        word1, word2 = word2, word3
        while word3 not in end_sent:
            if word.isalpha():
                word3 = choose_word_ahead(word1, word2)
                sent.append(word3)
                word1, word2 = word2, word3
            else:
                word3 = choose_word_ahead(prev_word1, word1, word2)
                word1, word2 = word2, word3
    return sent
    
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
    
def eval_size_words(sent_list):
    scored = {}
    ordered_sents = sorted(sent_list, key=len)
    if len(sent_list)%2:
       median = len(sent_list[len(sent_list/2)])
    else:
        first = len(sent_list[len(sent_list/2)-1])
        second = len(sent_list[len(sent_list/2)])
        median = (first+second)/2.0
    for sent in ordered_sents:
        scored[sent] = abs(len(sent)-median)
    return scored
   
def count_chars(sent):
    count = 0
    for w in sent:
        count += len(w)
    return count
      
def eval_size_chars(sent_list, max_size):
    scored = {}
    ordered_sents = sorted([s for s in sent_list if count_chars(s) <= max_size], key=count_chars)
    return ordered_sents

def eval_lm_sent(sent):
    sent.insert(0, "back1")
    sent.insert(0, "back2")
    prob = 1
    with sqlite3.connect(DB_LOC) as con:
        cur = con.cursor()
        for i in range(len(sent)-2):
            word1 = sent[i]
            word2 = sent[i+1]
            word3 = sent[i+2]
            unigram_prob = cur.execute("select probability from unigrams where word1=?", (word1,)).fetchone()
            if unigram_prob: 
                unigram_prob = unigram_prob[0]
            else:
                unigram_prob = 0
            bigram_prob = cur.execute("select probability from bigrams where word1=? and word2=?", (word1,word2)).fetchone()
            if bigram_prob: 
                bigram_prob = bigram_prob[0]
            else:
                bigram_prob = 0
            trigram_prob = cur.execute("select probability from trigrams where word1=? and word2=? and word3=?", (word1,word2,word3)).fetchone()
            if trigram_prob: 
                trigram_prob = trigram_prob[0]
            else:
                trigram_prob = 0
            interpolated = .9*trigram_prob + .09*bigram_prob + .01*unigram_prob
            prob *= interpolated
    return prob
    
def eval_lm(sent_list):
    ranked = []
    for sent in sent_list:
        ranked.append((sent, eval_lm_sent(sent)))
    ranked = sorted(ranked, key=itemgetter(1))
    return list(ranked[-1][0][2:])
    
def rejoin(word_list):
    padded = []
    for w in word_list:
        
        padded.append(w)
        if w[-1].isalpha():
            padded.insert(-1, " ")
    if padded[-1] == " ":
        padded = padded[:-1]
    return ''.join(padded)[1:]
    
def generate_sentence(seed, tag, num_candidates=5, iters=20, randomize=True):
    prev = []
    following = []
    max_len = 140-len(tag)-1
    for i in range(iters):
        try:
            candidate_prev = trigrams_back(seed, randomize)
            if candidate_prev not in prev:
                prev.append(candidate_prev)
        except TypeError:
            pass
        try:
            candidate_next = trigrams_forward(seed, randomize)
            if candidate_next not in following:
                following.append(candidate_next)
        except TypeError:
            pass
    prev = eval_size_chars(prev, max_len/2)[:-1]
    prev_index = (len(prev)-num_candidates)/2
    if prev_index > 0:
        prev=prev[prev_index:-prev_index]
    following = eval_size_chars(following, max_len/2)
    following_index = (len(following)-num_candidates)/2
    if following_index > 0:
        following=following[following_index:-following_index]
    prev = eval_lm(prev)
    following = eval_lm(following)
    prev = prev[:-1]
    prev.extend(following)
    return rejoin(prev)
    
