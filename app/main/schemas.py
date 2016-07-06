#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime

from marshmallow import Schema, fields, post_load, validates_schema, ValidationError

from . import models

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
MOBILE_PHONE_REGEX = re.compile(r'^(\+\d{1,3}[- ]?)?\d{11}$')

def check_email(email):
    return EMAIL_REGEX.match(email)

def check_mobile_phone(mobile_phone):
    return MOBILE_PHONE_REGEX.match(mobile_phone)

class ModelSchema(Schema):
    _id = fields.Method('get_id')
    # page = fields.Integer(dump_only=True)
    # next_num = fields.Integer(dump_only=True)
    # prev_num = fields.Integer(dump_only=True)

    def get_id(self, obj):
        return str(obj.id)

    def get_obj_class(self):
        return None

    # def set_instance(self, instance):
    #     self.context['instance'] = instance

    @post_load
    def deserialize(self, data):
        obj_class = self.get_obj_class()
        instance = self.context.get('instance')
        if obj_class:
            if instance:
                for k, v in data.items():
                    setattr(instance, k, v)

                return instance

            return obj_class(**data)

        return data

class NotificationSchema(ModelSchema):
    title = fields.String(required=True)
    body_raw = fields.String()
    from_whom = fields.String(required=True)
    to_whom = fields.List(fields.String(), required=True)
    is_draft = fields.Boolean(default=False)
    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)

    sent_email = fields.Boolean(default=False)
    sent_sms = fields.Boolean(default=False)
    extend_info = fields.Dict()

    def get_obj_class(self):
        return models.Notification

    @validates_schema
    def validate(self, data):
        if data.get('sent_email'):
            for to_one in data['to_whom']:
                try:
                    email = data['extend_info'][to_one].get('email')
                except:
                    raise ValidationError('No user named `{0}` in extend_info'.format(to_one))
                # if not email or not check_email(email):
                if email and not check_email(email):
                    raise ValidationError('email information error for {0}'.format(to_one))

        if data.get('sent_sms'):
            for to_one in data['to_whom']:
                try:
                    phone = data['extend_info'][to_one].get('phone')
                except:
                    raise ValidationError('No user named {0} in extend_info'.format(to_one))
                if phone and not check_mobile_phone(phone):
                    raise ValidationError('No phone number information for {0}'.format(to_one))



class NotificationActivitySchema(ModelSchema):
    # notification_title = fields.String(required=True, load_only=True)
    # from_whom = fields.String(required=True, load_only=True)
    # to_whom = fields.String(required=True, load_only=True)
    notification_title = fields.String(dump_only=True)
    from_whom = fields.String(dump_only=True)
    to_whom = fields.String(dump_only=True)
    is_read = fields.Boolean(default=False)
    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)

    def get_obj_class(self):
        return models.NotificationActivity

class NotificationActivityDetailSchema(NotificationActivitySchema):
    notification = fields.Nested(NotificationSchema, required=True)

