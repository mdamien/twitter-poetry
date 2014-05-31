import tweepy
import re

API_KEY = 'PqYOtC4RZwCN44OEzKhRj31cg'
API_SECRET = '5whWXtGWnPUYOwvzlvZaggfyyaRyjvHHEfYXSsxPiADmJyyNFu'

ACCESS_TOKEN = '2537768726-UFq9WrmA63ejHSlPPFAAONvSF5fifqCqaIyJKcY'
ACCESS_TOKEN_SECRET = 'O7NppDPJkAlq6zrjyYswhSKNLZcu3mqtFbKjJbz1OMNGe'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

WORDS = []
for x in open('words'):
    try:
        WORDS += [x.strip()]
    except UnicodeDecodeError:
        print x

def extract_words(tag):
    words = []
    #if lower case only, try to find words inside
    if tag.lower() == tag:
        for word in WORDS:
            try:
                if len(word) > 3 and word in tag.lower():
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
    trends = api.trends_place(1)
    tags = [x['name'] for x in trends[0]['trends'] if x['name'].startswith('#')]
    return [(x,extract_words(x)) for x in tags]

if __name__ == "__main__":
    print "Trending:"
    for tags, words in trends():
        print tags, words
