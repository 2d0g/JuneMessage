#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import request, current_app
from flask_mail import Message
import markdown2

from JuneMessage import mail
from JuneMessage.config import config


def send_mails(notification):
    recipients = [notification.extend_info[to_one].get('email') for to_one in notification.to_whom]
    recipients = filter(lambda x:x, recipients)
    if len(recipients) < 1:
        return

    msg = Message(notification.title)
    msg.sender = current_app._get_current_object().config['MAIL_USERNAME']
    msg.recipients = recipients

    msg.body = notification.body_raw
    msg.html = markdown2.markdown(notification.body_raw, extras=['code-friendly', 'fenced-code-blocks']).encode('utf-8')
        
    mail.send(msg)

