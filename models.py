#! /usr/bin/env python3
from peewee import *

db = SqliteDatabase('hikebot.db')

class MeetupGroup(Model):
    name = CharField()
    urlslug = CharField()

    class Meta:
        database = db

class MeetupEvent(Model):
    name = CharField()
    url = CharField()
    venue_name = CharField() 
    datetime = DateTimeField()
    endtime = DateTimeField(null=True)
    created = DateTimeField(null=True)
    description = TextField(null=True)
    meetup_id = CharField()
    yes_rsvp_count = IntegerField()
    waitlist_count = IntegerField()
    maybe_rsvp_count = IntegerField(null=True)
    group = ForeignKeyField(MeetupGroup, related_name='events')

    class Meta:
        database = db

class RedditPost(Model):
    event = ForeignKeyField(MeetupEvent, related_name='posts')
    title = CharField()
    reddit_id = CharField()

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([MeetupEvent, MeetupGroup, RedditPost])
