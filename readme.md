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


### Sample execution

        emily
        Trending topics: #LOXideas, #BradyBunch, #RickyDillonTo1Mill, #50FactsAboutMe, #lovemaya
        Topic choosen: #RickyDillonTo1Mill

        107  live tweets downloaded
        Seeds: following, getting, follow, forever, outside, give, people, please, mean, proud
        Trying seed: follow

        Tweet:
        Apparently with no to follow, or chase me if I should not fear the fight. #RickyDillonTo1Mill

        Do you want to tweet it ? (y/N): y
        Tweeted!

        $ emily
        Trending topics: #LOXideas, #BradyBunch, #RickyDillonTo1Mill, #50FactsAboutMe, #lovemaya
        Topic choosen: #lovemaya

        115  live tweets downloaded
        Seeds: express, sunday, tear, loud, writer, matters, continue, legacy, watch, arrive
        Trying seed: writer

        Tweet:
        Buzz the dull flies on the cause of early hurt, if such practised writer, you guessed, from the camp to purer reveille! #lovemaya

        Do you want to tweet it ? (y/N): y
        Tweeted!
