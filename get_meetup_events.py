#! /usr/bin/env python3
import meetup.api
import re
import datetime

import settings


client = meetup.api.Client()
key = settings.MEETUP_API_KEY
client.api_key = key


def parse_events(results):
    events = []
    regex = re.compile(settings.EVENT_IGNORE_REGEX)

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
