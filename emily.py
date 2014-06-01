import gen
import tweet
import sys
import magic_seeder
import random
from generate import generate_sentence

LIVE_FEED = True
TOPIC_MINING = False

if LIVE_FEED:
    topics = list(tweet.trends())
else:
    topics = [(u'#TanDificilEsQue', ['tan', 'que']), (u'#MariahNBC', ['mariah']), (u'#junewish', ['june', 'wish']), (u'#wits', []), (u'#FuerzaMontes', []), (u'#50ThingsAboutMyTwitterBestFriend', ['things', 'about', 'best', 'friend']), (u'#oRappaNoMultishow', []), (u'#KissConcert', ['kiss', 'concert'])]

print 'Trending topics:',
print ', '.join((tag for tag, words in topics))
tag, context = random.choice(topics)

print 'Topic choosen:', tag 

seed = magic_seeder.seed(tag)
print "Seed: ", seed
# result = gen.gen((seed,), tag)
result = generate_sentence(seed, tag)

print "Tweet:"
print
print result
print

answ = raw_input("Do you want to tweet it ? (y/N): ")
if answ.lower() == 'y':
    tweet.api.update_status(result)
    print "Tweeted!"
else:
    print "Not tweeted"
