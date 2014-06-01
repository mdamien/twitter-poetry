import gen
import tweet
import sys
import magic_seeder
import random
from generate import generate_sentence

FORCED_SEED = len(sys.argv) == 3
LIVE_FEED = not FORCED_SEED

if not FORCED_SEED:
    if LIVE_FEED:
        topics = list(tweet.trends())
    else:
        topics = [(u'#TanDificilEsQue', ['tan', 'que']), (u'#MariahNBC', ['mariah']), (u'#junewish', ['june', 'wish']), (u'#wits', []), (u'#FuerzaMontes', []), (u'#50ThingsAboutMyTwitterBestFriend', ['things', 'about', 'best', 'friend']), (u'#oRappaNoMultishow', []), (u'#KissConcert', ['kiss', 'concert'])]

    print 'Trending topics:',
    print ', '.join((tag for tag, words in topics))
    tag, context = random.choice(topics)
    print 'Topic choosen:', tag 
    seeds = magic_seeder.seed(tag)
else:
    tag = sys.argv[2]
    seed = sys.argv[1]
    seeds = (seed,)


while True:
    try:
        seed = random.choice(seeds)
        print " trying seed: ", seed
        result = generate_sentence(seed, tag)
        if 'ack1' in result or 'ack2' in result:
            raise Exception()
        break
    except (IndexError, Exception, StopIteration):
        print "...failed"

result += " "+tag

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
