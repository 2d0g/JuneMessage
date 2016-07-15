from flask import Blueprint

from . import api_views

main = Blueprint('main', __name__)

main.add_url_rule('/', 'index', api_views.index)

main.add_url_rule('/api/notifications/creation/', view_func=api_views.UserNotificationListView.as_view('create_notification'))
main.add_url_rule('/api/notifications/sent/', view_func=api_views.UserNotificationListView.as_view('send_notifications'))
main.add_url_rule('/api/notifications/received/', view_func=api_views.UserNotificationListView.as_view('received_notifications'), defaults={'is_sent':False})
main.add_url_rule('/api/notifications/sent/<pk>/', view_func=api_views.UserNotificationDetailView.as_view('send_notification'))
main.add_url_rule('/api/notifications/received/<pk>/', view_func=api_views.UserNotificationDetailView.as_view('received_notification'), defaults={'is_sent':False})
main.add_url_rule('/api/notifications/draft/', view_func=api_views.NotificationDraftListModifyDeleteView.as_view('notification_drafts'))
main.add_url_rule('/api/notifications/draft/<pk>/', view_func=api_views.NotificationDraftListModifyDeleteView.as_view('notification_draft'))
