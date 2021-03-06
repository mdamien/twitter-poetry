import tweepy
import re

key_file = '../keys.txt'

with open(key_file) as f:
    for line in f:
        line = line.strip()
        exec(line)

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

WORDS = []
for x in open('db/words'):
    WORDS += [x.strip()]

def extract_words(tag):
    words = []
    #if one case only, try to find words inside
    if tag.lower() == tag or tag.upper() == tag:
        for word in WORDS:
            try:
                if len(word) > 2 and word in tag.lower():
                    words += [word]
            except UnicodeDecodeError:
                pass
    else: #seperate by uppercase
        raw_words = [ word.lower() for word in re.findall('[A-Z][^A-Z]*', tag)]
        #filter non-english words
        for raw in raw_words:
            for word in WORDS:
                try:
                    if len(word) > 2 and raw == word:
                        words += [word]
                except UnicodeDecodeError:
                    pass
    return words


def trends():
    tags = set()
    for woeid in (23424977,):
        trends = api.trends_place(woeid)
        ts = set([x['name'] for x in trends[0]['trends'] if x['name'].startswith('#')])
        tags = tags | ts

    return [(x,extract_words(x)) for x in tags]

if __name__ == "__main__":
    print "Trending:"
    for tags, words in trends():
        print tags, words
