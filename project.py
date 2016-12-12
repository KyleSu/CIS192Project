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


def pull_info():
    TWEETS = 'http://twittercounter.com/pages/100'
    r = requests.get(TWEETS)
    soup = BeautifulSoup(r.text, "lxml")
    full_tag = soup.findAll('span', {"itemprop": True})
    l = list()
    for tag in full_tag:
        if "alternateName" in tag['itemprop']:
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
    else:
        print(request.form.get('name'))
        return json.dumps(False)
    return request.args.get('name')


@app.route('/searchhashtag', methods=['POST'])
def searchHashtag():
    print(request.form['hashtag'])


@app.route('/courses/<dept>')
@app.route('/courses/<dept>/<code>')
@app.route('/courses/<dept>/<code>/<section>')
def courses(dept, code=None, section=None):
    ''' Returns a list of courses matching the query parameters.

    The response should be JSON of the following format:
    { "results": [list of courses] }
    Each course in the list should be represented by a dictionary.

    ** Note that JSON should never have lists at the top level due to security
    issues with JavaScript! **
    See http://flask.pocoo.org/docs/security/#json-security.
    That's why we return a dictionary with one key/value pair instead.

    For any parameters not provided, match any value for that parameter.
    For instance, accessing /courses/cis should return a list of all CIS
    courses, and accessing courcies/cis/110 should return a list of all
    sections for CIS 110.

    There is also an optional GET request parameter for the 'type' key
    found in the CSV file. You should detect that and use it if it is provided.
    For instance, accessing /courses/cis?type=REC should return a list of all
    CIS recitation sections.
    '''

    '''return_list = []
    if code is None and section is None:
        if 'type' in request.args:
            return_list = [item for item in COURSES if item['dept'] == dept and
                           item['type'] == request.args.get('type')]
        else:
            return_list = [item for item in COURSES if item['dept'] == dept]
    elif code is None:
        if 'type' in request.args:
            return_list = [item for item in COURSES if item['dept'] == dept and
                           item['section'] == section and item['type'] == request.args.get('type')]
        else:
            return_list = [item for item in COURSES if item['dept'] == dept and
                           item['section'] == section]
    elif section is None:
        if 'type' in request.args:
            return_list = [item for item in COURSES if item['dept'] == dept and
                           item['code'] == code and item['type'] == request.args.get('type')]
        else:
            return_list = [item for item in COURSES if item['dept'] == dept and
                           item['code'] == code]
    else:
        if 'type' in request.args:
            return_list = [item for item in COURSES if item['dept'] == dept and
                           item['code'] == code and item['section'] == section and
                           item['type'] == request.args.get('type')]
        else:
            return_list = [item for item in COURSES if item['dept'] == dept and
                           item['code'] == code and item['section'] == section]
    data = {}
    data["results"] = return_list
    json_data = jsonify(data)

    return json_data'''


def main():
    pull_info()
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
