#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, URL, Optional
from flask_login import current_user
from flask_mongoengine.wtf import model_form

from . import models

class CreateMessageForm(Form):
    title = StringField('Title', validators=[Required()])
    to_whom = StringField('To', validators=[Required()])
    body_raw = TextAreaField('Content', validators=[Required()])
    email_required = BooleanField('Send Email')
    sms_required = BooleanField('Send SMS')
    
