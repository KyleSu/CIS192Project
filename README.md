# CIS192Project
In Twitter Bot, we parse through the HTMl of the website using BeautifulSoup,
www.twittercounter.com, in order to access the Twitter handle of
the top 100 users.

To store the data needed, there is a "users" dictionary and "hashtags" dictionary.
Each username will be stored as a key in the "users" dictionary,
and the value will be a dictionary of keys of hashtags and  values of the
count of each hashtag. 

In the "hashtags" dictionary, we store the hashtag as a key and the value as
an instance of our user created class, Hashtag, which stores information about
the text, the user and times the hashtag is used. This information is found using
the Twitter REST API to access the top 100 handles' tweets' qualities.

We use the generator to iterate through the list of Hashtag objects to count the
number of hashtags.

We overrode the __len__ magic method in order to get the number of times a
hashtag was used.
