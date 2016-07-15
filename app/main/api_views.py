#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.config import dictConfig
from datetime import datetime, timedelta
from flask import request, redirect, render_template, url_for, abort, flash, Blueprint, jsonify, current_app
from flask.views import MethodView

from flask_login import current_user, login_required

from . import models, schemas, signals, ext
from basic_auth import basic_auth_required
from JuneMessage.config import logging_config

dictConfig(logging_config)

logger = logging.getLogger()

def index():
    template_name = 'index.html'
    return render_template(template_name)

def jsonify_list_paginated(list_to_paginate, schema, list_name='result'):
    try:
        cur_page = int(request.args.get('page', 1))
    except:
        cur_page = 1


    per_page_default = current_app._get_current_object().config['PER_PAGE']
    per_page_max = current_app._get_current_object().config['PER_PAGE_MAX']
    try:
        per_page = int(request.args.get('per_page', per_page_default))
        if per_page > per_page_max:
            per_page = per_page_max
    except:
        per_page = per_page_default

    paginated_list = list_to_paginate.paginate(page=cur_page, per_page=per_page)
    result = {
        'page': paginated_list.page,
        'pages': paginated_list.pages,
        'total': paginated_list.total,
        'has_next': paginated_list.has_next,
        'has_prev': paginated_list.has_prev,
        'per_page': paginated_list.per_page,
        list_name: schema.dump(paginated_list.items).data
    }

    return jsonify(result)

class NotificationListView(MethodView):
    def get(self):
        notifications = models.Notification.objects.all()
        notification_schema = schemas.NotificationSchema(many=True)
        result = notification_schema.dump(notifications)

        return jsonify(notifications=result.data)

class UserNotificationListView(MethodView):
    decorators = [basic_auth_required, ]

    def get(self, is_sent=True):
        user = request.args.get('user')
        if not user:
            return 'Bad request', 400

        if is_sent:
            notification_activities = models.NotificationActivity.objects(from_whom=user, to_whom=None, sender=current_user.username)
        else:
            notification_activities = models.NotificationActivity.objects(to_whom=user, sender=current_user.username)
        

        schema = schemas.NotificationActivitySchema(many=True)

        # result = schema.dump(notification_activities)
        # return jsonify(notifications=result.data)

        return jsonify_list_paginated(notification_activities, schema, list_name='notifications')


    def post(self):
        data = request.get_json()
        schema = schemas.NotificationSchema()
        result = schema.load(data)
        if result.errors:
            return jsonify(result.errors), 400

        notification = result.data
        notification.sender = current_user.username

        # print type(notification)
        # print notification

        notification.save()
        if not notification.is_draft:
            signals.notification_created.send(current_app._get_current_object(), notification=notification)

        return jsonify(schema.dump(notification).data), 201

class UserNotificationDetailView(MethodView):
    decorators = [basic_auth_required, ]

    def get(self, pk, is_sent=True):
        user = request.args.get('user')
        if not user:
            return 'Bad request', 400

        if is_sent:
            notification_activity = models.NotificationActivity.objects.get_or_404(id=pk, from_whom=user, sender=current_user.username)
        else:
            notification_activity = models.NotificationActivity.objects.get_or_404(id=pk, to_whom=user, sender=current_user.username)
        
        schema = schemas.NotificationActivityDetailSchema()
        result = schema.dump(notification_activity)

        return jsonify(result.data)

    def put(self, pk, is_sent=False, partial=False):
        user = request.args.get('user')
        if not user:
            return 'Bad request', 400

        notification_activity = models.NotificationActivity.objects.get_or_404(id=pk, to_whom=user, sender=current_user.username)
        schema = schemas.NotificationActivitySchema(partial=partial)

        schema.context['instance'] = notification_activity

        data = request.get_json()
        result = schema.load(data)
        if result.errors:
            return jsonify(result.errors), 400

        notification_activity = result.data
        notification_activity.save()

        return jsonify(schema.dump(notification_activity).data)

    def patch(self, pk, is_sent=False):
        return self.put(pk, partial=True)

    def delete(self, pk, is_sent=False):
        user = request.args.get('user')
        if not user:
            return 'Bad request', 400

        notification_activity = models.NotificationActivity.objects.get_or_404(id=pk, to_whom=user, sender=current_user.username)
        notification_activity.delete()

        result = {'msg': 'No content found'}
        return jsonify(result), 204

class NotificationDraftListModifyDeleteView(MethodView):
    decorators = [basic_auth_required]

    def get(self, pk=None):
        user = request.args.get('user')
        if not user:
            return 'Bad request', 400

        if pk:
            notification = models.Notification.objects.get_or_404(pk=pk, from_whom=user, is_draft=True, sender=current_user.username)
            schema = schemas.NotificationSchema()
            result = schema.dump(notification)

            return jsonify(result.data)

        notifications = models.Notification.objects(from_whom=user, is_draft=True, sender=current_user.username)
        schema = schemas.NotificationSchema(many=True)
        # result = schema.dump(notifications)

        # return jsonify(drafts=result.data)
        return jsonify_list_paginated(notifications, schema, list_name='drafts')

    def put(self, pk, partial=False):
        user = request.args.get('user')
        if not user:
            return 'Bad request', 400

        notification = models.Notification.objects.get_or_404(pk=pk, from_whom=user, is_draft=True, sender=current_user.username)
        schema = schemas.NotificationSchema(partial=partial)
        schema.context['instance'] = notification

        data = request.get_json()
        result = schema.load(data)
        if result.errors:
            return jsonify(result.errors), 400

        notification = result.data

        notification.save()
        if not notification.is_draft:
            signals.notification_created.send(current_app._get_current_object(), notification=notification)


        return jsonify(schema.dump(notification).data)

    def patch(self, pk):
        return self.put(pk, partial=True)


    def delete(self, pk):
        user = request.args.get('user')
        if not user:
            return 'Bad request', 400

        notification = models.Notification.objects.get_or_404(pk=pk, from_whom=user, is_draft=True, sender=current_user.username)
        notification.delete()

        result = {'msg': 'No content found'}
        return jsonify(result), 204
