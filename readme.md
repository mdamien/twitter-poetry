twitter-poetry
===============

Generating tweets in the style of Emily Dickinson automatically on trending topics

- `emily.py`

Generate tweet on random topic: `python2 emily.py`
Generate tweet on specifc topic `python2 emily.py "#fun"`
Generate tweet on specific topic with specific seed `python2 emily.py love "#ThisIsMariah"`

- `tweet.py`: Communication with twitter (get trending topics, post status)
- `magic_seeder.py`: Topic analysis to find the most defining words of the topic
- `generate.py`: Using N-gram algorithm to build the tweet
