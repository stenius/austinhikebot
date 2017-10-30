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

if __name__ == '__main__':
    events = client.GetEvents({'group_urlname': 'Austin-Sierra-Club-Outings'})
    parse_events(events.results)
