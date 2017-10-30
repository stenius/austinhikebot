#! /usr/bin/env python3
import meetup.api
import re
import datetime

from settings import MEETUP_API_KEY


client = meetup.api.Client()
key = MEETUP_API_KEY
client.api_key = key


def parse_events(results):
    events = []
    regex = re.compile(r'Bouldering|Meeting|Book Club|([D|d]ocumentary)|([S|s]creening)|Town Lake|Shoal Creek')

    for event in results:
        if re.search(regex, event['name']):
            pass
        else:
            date = datetime.datetime.fromtimestamp(event['time']/1000.)
            if date < (datetime.datetime.now() + datetime.timedelta(days=365)):
                events.append(event)
    return events

def get_event_post_title(event, group_name='', show_venue_name=True):
    name = event['name']
    venue_name = event['venue']['name']
    date = datetime.datetime.fromtimestamp(event['time']/1000.)
    date_str = date.strftime('%x %I:%M%p')

    #show how many people are attending event
    if 'rsvp_limit' in event:
        rsvp_string = str(event['yes_rsvp_count']) + '/' + str(event['rsvp_limit'])
    else:
        rsvp_string = event['yes_rsvp_count']

    if show_venue_name:
        return '[%s] %s %s %s' % (date_str, group_name, name, venue_name)
    else:
        return '[%s] %s %s' % (date_str, group_name, name)

if __name__ == '__main__':
    events = client.GetEvents({'group_urlname': 'Austin-Sierra-Club-Outings'})
    parse_events(events.results)
