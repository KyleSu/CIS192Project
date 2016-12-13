# CIS192Project, Claire Huang & Kyle Su
The purpose of Twitter Bot is to take the top 100 most followed accounts on Twitter
and collect their most recent tweets to track hashtag usage. Our app displays for each user
all hashtags used, as well as number of times used. For individual hashtags, our app displays
all users that used that hashtag in addition to the number of uses per user, and total.

Our homepage has two search bars. You can either search by Twitter user name, or by specific
hashtags. Capitalization matters. If you searched for a valid user, you'll see a list of all
hashtags that user has used in their past XX tweets (modifiable upto past 200), as well as
the number of times each hashtag was used. There will also be a link to that Twitter account's
page. If you enter a valid hashtag, you will see a list of all users who have used the tag,
as well as the total number of times the tag was used. Our homepage also displays the sum total
of all hashtags used, as well as the ten most popular hashtags by number of mentions.

Modules used:
    json - Used to return False data in AJAX calls
    functools - Used to override rich comparision magic methods
    operator - Used to sort items
    flask - Used to route URLs, pass data back and forth from frontend to backend
    requests - Used to access information passed from frontend
    bs4 - Used BeautifulSoup to crawl websites to find Twitter usernames
    tweepy - Used to ease usage of Twitter API

Custom class requirement:
    We implemented a Hashtag class to store information about individual hashtags. The "text"
field stores the actual string of the hashtag. The "count" field tracks the total number of times
the hashtag was used by all users. The "users" field is a dictionary with keys="username",
value="# times this hashtag was used by that username".
    We overrode the rich comparision magic methods (unused), as well as the __len__ method. We
used our __len__ method to return the "count" of the object, which is used to accumulate the
total number of times all hashtags are used (displayed on our homepage).

Generator function requirement:
    In pull_info() we used a generator function to accumulate the total number of hashtags used.
Instead of creating another list of all the individual Hashtag objects (which are containe in a
dictionary), we used the generator to iterate through the objects one by one.

