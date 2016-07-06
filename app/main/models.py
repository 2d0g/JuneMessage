#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import markdown2

from JuneMessage import db

# class Message(db.Document):
#     title = db.StringField(required=True)
#     body_raw = db.StringField()
#     body_rich = db.StringField()
#     from_whom = db.StringField(default='admin')
#     to_whom = db.StringField(required=True)
#     is_read = db.BooleanField(default=False)
#     is_draft = db.BooleanField(default=False)
#     create_time = db.DateTimeField(required=True, default=datetime.datetime.now())
#     update_time = db.DateTimeField(required=True, default=datetime.datetime.now())

#     def save(self, *args, **kwargs):
#         self.body_rich = markdown2.markdown(self.body_raw, extras=['code-friendly', 'fenced-code-blocks']).encode('utf-8')
#         return super(Message, self).save(*args, **kwargs)

#     def __unicode__(self):
#         return self.title

#     meta = {
#         'allow_inheritance': True,
#         # 'indexes': ['title'],
#         'ordering': ['-update_time']
#     }

extend_default = {'username':{'email':'aaa@aa.aa', 'phone':'123456789'}}

class Notification(db.Document):
    title = db.StringField(required=True)
    body_raw = db.StringField()
    # body_rich = db.StringField()
    from_whom = db.StringField(default='admin')
    to_whom = db.ListField(db.StringField(), required=True)
    is_draft = db.BooleanField(default=False)
    create_time = db.DateTimeField()
    update_time = db.DateTimeField()

    sender = db.StringField(default='JuneMessage')

    sent_email = db.BooleanField(default=False)
    sent_sms = db.BooleanField(default=False)
    extend_info = db.DictField(default=extend_default)

    def save(self, *args, **kwargs):
        # self.body_rich = markdown2.markdown(self.body_raw, extras=['code-friendly', 'fenced-code-blocks']).encode('utf-8')
        if not self.create_time:
            self.create_time = datetime.datetime.now()
        self.update_time = datetime.datetime.now()
        return super(Notification, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        # 'indexes': ['title'],
        'ordering': ['-update_time']
    }

class NotificationActivity(db.Document):
    '''
    This model is for message receiver and sender to act with messages
    '''
    notification = db.ReferenceField(Notification)
    notification_title = db.StringField()
    from_whom = db.StringField()
    to_whom = db.StringField() # This field will be none for message sender
    sender = db.StringField(default='JuneMessage')
    is_read = db.BooleanField(default=False)
    create_time = db.DateTimeField()
    update_time = db.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.create_time:
            self.create_time = datetime.datetime.now()
        self.update_time = datetime.datetime.now()
        return super(NotificationActivity, self).save(*args, **kwargs)

    meta = {
        'allow_inheritance': True,
        'ordering': ['-update_time']
    }
