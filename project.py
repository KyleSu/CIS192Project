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
from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from twitter import *

consumer_key = "ssf7gtajPE8HRwsaWcEeVaOxh"
consumer_secret = "	mFlYP2OtVuy5egZcxskh5R60MA3DpRpYHz21YyuUSu1023KBnN"
access_key = "	808414961940758528-NYjteAFIdUjx5jaYeQYfB5bfuxJhDvS"
access_secret = "ihMzFIXTiqlaMwjoza76YeVYT9n3nlSKs5AQnnSZqfZrB"

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


users = {}
hashtags = {}

def get_tweets(username):
  TWEETS = 'http://twittercounter.com/pages/100'
  r = requests.get(TWEETS)
  soup = BeautifulSoup(r.text, "lxml")
  full_tag = soup.findAll('span',{"itemprop":True})
  l = list()
  twitter = Twitter(
		auth = OAuth(config[access_key], config[access_secret], config[consumer_key], config[consumer_secret]))

  for tag in full_tag:
    if "alternateName" in tag['itemprop']:
        tag.text[1:] = {}
        l.append(tag.text[1:])
  r.connection.close()
  print (l)

def pull_info():
    TWEETS = 'http://twittercounter.com/pages/100'
    r = requests.get(TWEETS)
    soup = BeautifulSoup(r.text, "lxml")
    full_tag = soup.findAll('span', {"itemprop": True})
    l = list()
    for tag in full_tag:
        if "alternateName" in tag['itemprop']:
            get_tweets(tag.text[1:])
            l.append(tag.text[1:])
    r.connection.close()
    '''print (l)'''


@app.route('/')
def home():
    '''This is what you will see if you go to http://127.0.0.1:5000.'''
    return render_template('index.html')


@app.route('/searchuser', methods=['POST'])
def searchUser():
    if request.form.get('name') in users:
        user = request.form.get('name')
        sorted_hashtags = sorted(users[user].items(), key=operator.itemgetter(1))
        return render_template('user.html', username=user, hashtags=sorted_hashtags)
    else:
        sorted_hashtags = [('a', 5), ('b', 6)]
        return render_template('user.html', username="hello", hashtags=sorted_hashtags)
        print(request.form.get('name'))
        return json.dumps(False)


@app.route('/searchhashtag', methods=['POST'])
def searchHashtag():
    print(request.form['hashtag'])


def main():
    '''pull_info()'''
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
