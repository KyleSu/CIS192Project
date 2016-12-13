''' Homework 10
-- Due Tuesday, November 22 at 11:59pm
-- Before starting, read
https://www.cis.upenn.edu/~cis192/homework/
-- Always write the final code yourself
-- Cite any websites you referenced
-- Use the PEP-8 checker for full style points:
https://pypi.python.org/pypi/pep8
'''

# In this HW, you'll create an API for serving basic information about Penn
# courses. Note that the provided csv file is a few years old...
#
# First, you'll convert a CSV file containing Registrar data to JSON
# format.  Next, you'll use this data as a source for serving through
# your API.  Helper functions will probably be useful!


import json
import functools
import operator
from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import tweepy
from tweepy import OAuthHandler

consumer_key = "ssf7gtajPE8HRwsaWcEeVaOxh"
consumer_secret = "mFlYP2OtVuy5egZcxskh5R60MA3DpRpYHz21YyuUSu1023KBnN"
access_key = "808414961940758528-XScUDlrETfGl1nuoTcjOSCITPSFLdeg"
access_secret = "zVFnizTlmtCR4gHGWJI9NEslNzgqkipdJhqdNDHvNhlP2"

app = Flask(__name__)


@functools.total_ordering
class Hashtag:
    def __init__(self, text):
        self.text = text
        self.count = 0
        self.users = {}

    def addTweet(self, user):
        if user in self.users:
            newCount = self.users[user] + 1
            self.users[user] = newCount
            self.count += 1
        else:
            self.users[user] = 1
            self.count += 1

    def __eq__(self, other):
        return (self.count == other.count)

    def __ne__(self, other):
        return (self.count != other.count)

    def __gt__(self, other):
        return (self.count > other.count)

    def __len__(self):
        return self.count


users = {}
hashtags = {}
topten_hashtags = []
topten_data = []
total_hashtags = 0


def get_tweets(username):
    if username not in users:
        users[username] = {}
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    new_tweets = api.user_timeline(screen_name=username, count=50)
    for status in new_tweets:
        list_text = status.entities.get('hashtags')
        for dict_item in list_text:
            hashtag_text = dict_item.get('text')
            ''' Update users dictionary '''
            if hashtag_text in users[username]:
                new_count = users[username][hashtag_text] + 1
                users[username][hashtag_text] = new_count
            else:
                users[username][hashtag_text] = 1
            ''' Update hashtags dictionary '''
            if hashtag_text in hashtags:
                hashtags[hashtag_text].addTweet(username)
            else:
                new_hashtag = Hashtag(hashtag_text)
                hashtags[hashtag_text] = new_hashtag
                hashtags[hashtag_text].addTweet(username)

def pull_info():
    TWEETS = 'http://twittercounter.com/pages/100'
    r = requests.get(TWEETS)
    soup = BeautifulSoup(r.text, "lxml")

    l = list()
    full_tag = soup.findAll('span', {"itemprop": True})

    for tag in full_tag:
        if "alternateName" in tag['itemprop']:
            get_tweets(tag.text[1:])
            l.append(tag.text[1:])

    r.connection.close()

    hashtag_counter = (len(hashtag_object) for hashtag_object in hashtags.values())
    global total_hashtags
    for x in range(0, len(hashtags.keys())):
        total_hashtags += next(hashtag_counter)
    topten_hashtags = sorted(hashtags.values(), key=operator.attrgetter('count'), reverse=True)[:10]

    for i in range(len(topten_hashtags)):
        hashtag_object = topten_hashtags[i]
        hashtag_data = (getattr(hashtag_object, 'text'), getattr(hashtag_object, 'count'))
        topten_data.append(hashtag_data)

@app.route('/')
def home():
    '''This is what you will see if you go to http://127.0.0.1:5000.'''
    global total_hashtags

    return render_template('index.html', num_hashtags=total_hashtags, topten_data=topten_data)


@app.route('/searchuser', methods=['POST'])
def searchUser():
    if request.form.get('name') in users:
        user = request.form.get('name')
        sorted_hashtags = sorted(users[user].items(), key=operator.itemgetter(1), reverse=True)
        return render_template('user.html', username=user, hashtags=sorted_hashtags)
    else:
        return json.dumps(False)


@app.route('/searchhashtag', methods=['POST'])
def searchHashtag():
    if request.form.get('hashtag') in hashtags:
        tag = request.form.get('hashtag')

        hashtag_object = hashtags[tag]
        num_uses = getattr(hashtag_object, 'count')
        unsorted_users = getattr(hashtag_object, 'users')
        sorted_users = sorted(unsorted_users.items(), key=operator.itemgetter(1), reverse=True)

        return render_template('hashtag.html', tag=tag, num_uses=num_uses, users=sorted_users)
    else:
        return json.dumps(False)


def main():
    pull_info()
    app.debug = False
    app.run()


if __name__ == "__main__":
    main()
