#! /usr/bin/env python3
import praw

from get_meetup_events import *
from settings import *

if __name__ == '__main__':
    reddit = praw.Reddit(client_id=REDDIT_APP_ID,
        client_secret=REDDIT_APP_SECRET,
        user_agent='HikeBot',
        username=REDDIT_APP_USERNAME,
        password=REDDIT_APP_PASSWORD)
    subreddit = reddit.subreddit('austinhiking')

    events = client.GetEvents({'group_urlname': 'Austin-Sierra-Club-Outings'})
    filtered_events = parse_events(events.results)
    for event in filtered_events:
        title = get_event_post_title(event, group_name='Austin Sierra Club:', show_venue_name=False)
        subreddit.submit(title=title, url=event['event_url'])

    events = client.GetEvents({'group_urlname': 'OUTSIDEinTexas'})
    filtered_events = parse_events(events.results)
    for event in filtered_events:
        title = get_event_post_title(event, group_name='Outside In Texas:', show_venue_name=False)
        subreddit.submit(title=title, url=event['event_url'])

    events = client.GetEvents({'group_urlname': 'backpackers-170'})
    filtered_events = parse_events(events.results)
    for event in filtered_events:
        title = get_event_post_title(event, group_name='Austin Backpackers:', show_venue_name=False)
        subreddit.submit(title=title, url=event['event_url'])
