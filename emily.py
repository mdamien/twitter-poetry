import gen
import tweet
import sys
import magic_seeder
import random
from generate import generate_sentence

FORCED_TAG = len(sys.argv) == 2
FORCED_SEED = len(sys.argv) == 3
LIVE_FEED = not FORCED_SEED and not FORCED_TAG

print
print
if not FORCED_SEED:
    if not FORCED_TAG:
        topics = list(tweet.trends())
        print 'Trending topics:',
        print ', '.join((tag for tag, words in topics))
        with open('db/used_tags','r') as used:
            useds = set(w.strip() for w in used)
            new_topics = list((t,w) for t,w in topics if t not in useds)
            if len(new_topics) > 0:
                topics = new_topics
        topics = list((t,w) for t,w in topics if t.startswith('#'))
        print 'Topic filtered:',
        print ', '.join((tag for tag, words in topics))
        tag, context = random.choice(topics)
        print 'Topic choosen:', tag 
        seeds = magic_seeder.seed(tag)
    else:
        tag = sys.argv[1]
        seeds = magic_seeder.seed(tag)
else:
    tag = sys.argv[2]
    seed = sys.argv[1]
    seeds = (seed,)


while True:
    try:
        seed = random.choice(seeds)
        print "Trying seed:", seed
        result = generate_sentence(seed, tag)
        if 'ack1' in result or 'ack2' in result:
            raise Exception()
        break
    except (IndexError, Exception, StopIteration):
        with open('db/bad_seeds','a') as bads:
            bads.write(seed+'\n')
        print " -> failed (added to blacklist)"

result += " "+tag

print
print "Tweet:"
print result
print

answ = raw_input("Do you want to tweet it ? (y/N): ")
if answ.lower() == 'y':
    tweet.api.update_status(result)
    with open('db/used_tags','a') as used:
        used.write(tag+'\n')
    print "Tweeted!"
else:
    print "Not tweeted"
