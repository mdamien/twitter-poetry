import gen
import tweet
import sys
import seeder
import random

LIVE_FEED = False
TOPIC_MINING = False

if LIVE_FEED:
    topics = list(tweet.trends())
else:
    topics = [(u'#TanDificilEsQue', ['tan', 'que']), (u'#MariahNBC', ['mariah']), (u'#junewish', ['june', 'wish']), (u'#wits', []), (u'#FuerzaMontes', []), (u'#50ThingsAboutMyTwitterBestFriend', ['things', 'about', 'best', 'friend']), (u'#oRappaNoMultishow', []), (u'#KissConcert', ['kiss', 'concert'])]

print 'Trending topics:',
print ', '.join((tag for tag, words in topics))
topics = list((tag,words) for tag, words in topics if len(words) > 0)

print 'Valid topics:   ',
print ', '.join(("%s (%s)" % (tag, len(words)) for tag, words in topics))

if TOPIC_MINING:
    print 'Topic mining..  :'

    topics_mined = []
    for tag, words in topics:
        all_seeds = set(words)
        for word in words:
            if len(all_seeds) > 2:
                break
            seeds = seeder.seeds(word)
            if len(seeds):
                all_seeds |= set(seeds)
        if len(all_seeds) > 0:
            topics_mined.append((tag, all_seeds))
    topics = topics_mined

print "Topics processed:"
for tag, words in topics:
    print "    ",tag,':',', '.join(words)

if len(topics) == 0:
    print "No valid topics, aborting"
    sys.exit(0)
tag, context = random.choice(topics)

print 'Topic choosen:', 
print tag, '(',', '.join(context),')' 

result = gen.gen(context, tag)

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
