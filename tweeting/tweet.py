import tweepy
import re

API_KEY = 'KxDwx51HAE0eheL41CdwIsdcX'
API_SECRET = 'R53A5YJgBZlSdLcAgMlZhsPO6p3hIQmvUazD2yUDdutfNZDyTY'

ACCESS_TOKEN = '2537768726-TjOpFSZFwZItRClECxjJ1tbIdJVbAyzTAmPGHvN'
ACCESS_TOKEN_SECRET = 'ec38puj073WwxWtX1bHb2HWro7BqVdHJOy46my14yLusy'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

WORDS = []
for x in open('words'):
    WORDS += [x.strip()]

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
    tags = set()
    for woeid in (1, 23424977):
        trends = api.trends_place(woeid)
        ts = set([x['name'] for x in trends[0]['trends'] if x['name'].startswith('#')])
        tags = tags | ts

    return [(x,extract_words(x)) for x in tags]

if __name__ == "__main__":
    print "Trending:"
    for tags, words in trends():
        print tags, words
