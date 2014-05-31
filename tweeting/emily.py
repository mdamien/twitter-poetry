import gen
import tweet
import random

topics = tweet.trends()
print 'Trending topics:',
print ','.join((tag for tag, words in topics))
topics = ((tag,words) for tag, words in topics if len(topics) > 0)
print 'Valid topics:   ',
print ','.join((tag for tag, words in topics))
topic = random.choice(topics)
print 'Topic choosen:', 

