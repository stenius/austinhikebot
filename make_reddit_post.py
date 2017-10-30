#! /usr/bin/env python3
import praw

from get_meetup_events import *
import settings
from models import *

if __name__ == '__main__':
    '''get events from meetup and make reddit posts'''

    reddit = praw.Reddit(client_id=settings.REDDIT_APP_ID,
        client_secret=settings.REDDIT_APP_SECRET,
        user_agent='HikeBot',
        username=settings.REDDIT_APP_USERNAME,
        password=settings.REDDIT_APP_PASSWORD)
    subreddit = reddit.subreddit(settings.REDDIT_SUBREDDIT)

    for meetupgroup in settings.MEETUP_GROUPS:
        group, group_created = MeetupGroup.get_or_create(
                urlslug=meetupgroup['urlslug'],
                defaults={
                    'name': meetupgroup['name'],
                }
            )
        events = client.GetEvents({'group_urlname': meetupgroup['urlslug']})
        filtered_events = parse_events(events.results)
        for event_result in filtered_events:
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
            title = event.get_post_title(show_venue_name=False)
            print(title)
            if not RedditPost.filter(event=event).count():
                if MeetupEvent.filter(datetime__gte=datetime.datetime.now(),
                        name=event_result['name']).count() < 5:
                    print('\tcreated event')
                    submission = subreddit.submit(title=title, url=event_result['event_url'])
                    reddit_post = RedditPost.create(event=event, title=title,
                            reddit_id=submission.id)
                else:
                    print('\tskipping event')
                    pass
                    # TODO: post updated information to post
                    # reddit_post = RedditPost.get(RedditPost.event=event)
                    # submission = reddit.submission(id=submission.id)
            else:
                print('\talready posted')
