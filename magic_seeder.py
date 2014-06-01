import tweet
import sys
import gen
import pickle
from collections import defaultdict, Counter
from operator import itemgetter
from sklearn.feature_extraction.text import TfidfVectorizer
import random
from tfidf import *

emily_weight = .6
tweet_weight = .4

COMMON = list(w.strip() for w in open('db/words').readlines()[:100])

def clean(status):
    status = list(word for word in status.split()) 
    status = list(word for word in status if len(word) > 3 and word.lower() in tweet.WORDS and not  word  in COMMON)
    #filter spam
    for word in status:
        if word.upper() == word and word.lower() in tweet.WORDS:
            return None
    status = list(word.lower() for word in status)
    return status

def seed(tag):
    #get tweets
    if False:
        output = open('st.pkl','rb')
        statuses = pickle.load(output)
    else:
        statuses = []
        statuses = tweet.api.search(tag+' +exclude:retweets', count=100, result_type='mixed', lang='en')
        print len(statuses), ' live tweets downloaded'
    
    #clean them
    statuses = [clean(status.text) for status in statuses if not status.text.startswith('RT')]
    statuses = [s for s in statuses if s]
    tokens = []
    for s in statuses:
        for w in s:
            tokens.append(w.strip())
            
    token_counts = Counter(tokens)
    total_tokens = float(sum(token_counts.itervalues()))
    unique_tokens = set(tokens)
    tag_probs = {}
    idf_con = sqlite3.connect(idf_db_loc)
    idf_cur = idf_con.cursor()
    print "Starting seed generation"
    for token in unique_tokens:
        to_add = True
        try:
            prob = emily_weight * idf_cur.execute("select score from emily_tfidf where word=?", (token,)).fetchone()[0]
        except (IndexError, TypeError):
            prob = emily_weight * tfidf_emily(token)
        if not prob:
            to_add = False
        try:
            idf = idf_cur.execute("select score from idf where word=?", (token,)).fetchone()[0]
        except (IndexError, TypeError):
            idf = get_idf(token)
        token_tf = tf_tag(token, token_counts[token], total_tokens)
        tweet_tfidf = tweet_weight * idf * token_tf
        if not tweet_tfidf:
            to_add = False
        prob += tweet_tfidf
        if to_add:
            tag_probs[token] = prob
    idf_con.close()
    print "Tf/Idf complete"
    
#     #let's begin the magic
#     def tokenize(text):
#         return text.split()
# 
#     token_dict = {
#             'corpus' : gen.corpus,
#             'tweets' : ' '.join(tokens)
#             }
# 
#     tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
#     tfs = tfidf.fit_transform(token_dict.values())
# 
#     feature_names = tfidf.get_feature_names()
#     comb = []
#     for col in tfs.nonzero()[1]:
#         if tfs[0,col] > 0:
#             comb.append((feature_names[col], tfs[0, col]))
# 
#     prob = lambda x: x[1]
#     comb = list(set(reversed(sorted(comb, key=prob))))
    comb = sorted(tag_probs.iteritems(), key=itemgetter(1), reverse=True) 
    
    print "Seeds: "
    for c,p in comb[:10]:
        print "X" if c in gen.corpus else "_",c,p
    top = []
    for c,p in comb:
        if c in gen.corpus:
            top.append(c)
        if len(top) > 5:
            break
    return top
