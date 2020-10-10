# Austin Hike Bot

This code is no longer functional.  Meetup has changed their API and started requiring payment for it.

Bot for pulling events for various public hikes into [r/AustinHiking](https://www.reddit.com/r/AustinHiking/)

This bot queries meetup.com for events in specific groups, checks them against
a regex blacklist, and then posts a link to reddit.com.

## Requirements

* Python3
* [Python API for Meetup](//github.com/pferate/meetup-api)
* [Python Reddit API Wrapper](https://praw.readthedocs.org/)
* [Peewee: a litte orm](http://github.com/coleifer/peewee/)

## Setup and usage

* Install requirements from `requirements.txt` file.
* run `models.py` to setup the db
* edit settings file to add API keys and group information
* run `make_reddit_post.py` to see for all events in your meetup group and make posts

## Settings

Create a file called `settings.py` and store your api keys and settings there.

```
MEETUP_API_KEY = '111111111111111111111111111111'

REDDIT_APP_SECRET = '111111111111111111111111111'
REDDIT_APP_ID = '11111111111111'
REDDIT_APP_USERNAME = '1111111'
REDDIT_APP_PASSWORD = '1111111111111111'
REDDIT_SUBREDDIT = 'austinhiking'

EVENT_IGNORE_REGEX = r'Bouldering|Meeting|Book Club|([D|d]ocumentary)|([S|s]creening)|Town Lake|Shoal Creek'
MEETUP_GROUPS = [
    {
        'urlslug':'Austin-Sierra-Club-Outings',
        'name':'Austin Sierra Club',
    },
    {
        'urlslug':'OUTSIDEinTexas',
        'name':'Outside In Texas',
    },
]
```
