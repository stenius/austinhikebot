#! /usr/bin/env python3
import meetup.api
import re
import datetime

import settings


client = meetup.api.Client()
key = settings.MEETUP_API_KEY
client.api_key = key


def parse_events(results):
    '''filters meetup api response events to determine if the name passes the
       ignore regex'''

    regex = re.compile(settings.EVENT_IGNORE_REGEX)

    return [event for event in results if not re.search(regex, event['name'])]

if __name__ == '__main__':
    '''grab event and test filtering events'''
    events = client.GetEvents({'group_urlname': 'Austin-Sierra-Club-Outings'})
    print(parse_events(events.results))
