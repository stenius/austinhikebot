#! /usr/bin/env python3
import praw

from get_meetup_events import *
from settings import *
from models import *

if __name__ == '__main__':
    reddit = praw.Reddit(client_id=REDDIT_APP_ID,
        client_secret=REDDIT_APP_SECRET,
        user_agent='HikeBot',
        username=REDDIT_APP_USERNAME,
        password=REDDIT_APP_PASSWORD)
    subreddit = reddit.subreddit('austinhiking')

    meetup_groups = [
        {
            'urlslug':'Austin-Sierra-Club-Outings',
            'name':'Austin Sierra Club',
        },
        {
            'urlslug':'OUTSIDEinTexas',
            'name':'Outside In Texas',
        },
        {
            'urlslug':'backpackers-170',
            'name':'Austin Backpackers',
        },
        {
            'urlslug':'hiking-586',
            'name':'COD Hiking',
        },
        {
            'urlslug':'Hiking-For-Tacos',
            'name':'HFT',
        },
    ]

    for meetupgroup in meetup_groups:
        group, group_created = MeetupGroup.get_or_create(
                urlslug=meetupgroup['urlslug'],
                defaults={
                    'name': meetupgroup['name'],
                }
            )
        events = client.GetEvents({'group_urlname': meetupgroup['urlslug']})
        filtered_events = parse_events(events.results)
        for event_result in filtered_events:
            title = get_event_post_title(event_result, group_name='%s:'%meetupgroup['name'], show_venue_name=False)
            print(title)
            if MeetupEvent.filter(datetime__gte=datetime.datetime.now(),
                    name=event_result['name']).count() < 5:
                event, event_created = MeetupEvent.get_or_create(
                        meetup_id=event_result['id'],
                        url=event_result['event_url'],
                        group=group,
                        defaults={
                            'name': event_result['name'],
                            'venue_name': event_result['venue']['name'],
                            'datetime': datetime.datetime.fromtimestamp(event_result['time']/1000.),
                            'created': datetime.datetime.fromtimestamp(event_result['created']/1000.),
                            'description': event_result['description'],
                            'yes_rsvp_count': event_result['yes_rsvp_count'],
                            'waitlist_count': event_result['waitlist_count'],
                            'maybe_rsvp_count': event_result['maybe_rsvp_count'],
                        }
                    )
                if event_created:
                    print('\tcreated event')
                    submission = subreddit.submit(title=title, url=event_result['event_url'])
                    reddit_post = RedditPost.create(event=event, title=title,
                            reddit_id=submission.id)
                else:
                    print('\tskipping event')
                    pass
                    # reddit_post = RedditPost.get(RedditPost.event=event)
                    # submission = reddit.submission(id=submission.id)
