#! /usr/bin/env python3
from peewee import *

db = SqliteDatabase('hikebot.db')

class BaseModel(Model):
    class Meta:
        database = db

class MeetupGroup(BaseModel):
    name = CharField()
    urlslug = CharField()

class MeetupEvent(BaseModel):
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

    def get_post_title(self, show_venue_name=True):
        '''returns the title that gets posted to reddit'''
        name = self.name
        venue_name = self.venue_name
        date = self.datetime
        date_str = date.strftime('%x %I:%M%p')

        if show_venue_name:
            return '[%s] %s: %s %s' % (date_str, self.group.name, name, venue_name)
        else:
            return '[%s] %s: %s' % (date_str, self.group.name, name)

class RedditPost(BaseModel):
    event = ForeignKeyField(MeetupEvent, related_name='posts')
    title = CharField()
    reddit_id = CharField()


if __name__ == '__main__':
    db.connect()
    db.create_tables([MeetupEvent, MeetupGroup, RedditPost])
