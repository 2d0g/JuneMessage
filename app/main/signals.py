from flask import request, current_app
from blinker import Namespace

from . import models, ext

maymessage_signals = Namespace()
notification_created = maymessage_signals.signal('notification-created')

def create_notification_activity(notification, from_whom, to_whom, is_read=False):
    notification_activity = models.NotificationActivity()
    notification_activity.notification = notification
    notification_activity.notification_title = notification.title
    notification_activity.from_whom = from_whom
    notification_activity.to_whom = to_whom
    notification_activity.is_read = is_read
    notification_activity.sender = notification.sender

    notification_activity.save()

    return notification_activity

@notification_created.connect
def on_notification_created(sender, notification, **extra):
    # notification activity for sender
    create_notification_activity(notification=notification, from_whom=notification.from_whom, to_whom=None, is_read=True)

    # notification activity for receiver
    for to_one in notification.to_whom:
            create_notification_activity(notification=notification, from_whom=notification.from_whom, to_whom=to_one)

    if notification.sent_email:
        ext.send_mails(notification)

    if notification.sent_sms:
        ext.send_sms(notification)