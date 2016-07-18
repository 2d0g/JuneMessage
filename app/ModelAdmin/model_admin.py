#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin import AdminIndexView
from flask_admin.contrib.mongoengine import ModelView
from flask_login import current_user

# from JuneMessage import admin
from accounts import models as accounts_models
from main import models as main_models
from oauth2 import models as oauth2_models

# Create customized model view class
class GeneralModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
        # return current_user.is_superuser


# Create customized index view class
class GeneralAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
        # return current_user.is_superuser

def register_admin_views(admin):
    # accounts_views = [GeneralModelView(accounts_models.User)]
    # main_views = [GeneralModelView(main_models.Notification), GeneralModelView(main_models.NotificationActivity)]
    # oauth_views = [GeneralModelView(oauth2_models.Client), GeneralModelView(oauth2_models.Grant), 
    #     GeneralModelView(oauth2_models.Token)]

    # admin.add_views(*accounts_views)
    # admin.add_views(*main_views)
    # admin.add_views(*oauth_views)
    admin.add_view(GeneralModelView(accounts_models.User, category='accounts'))

    admin.add_view(GeneralModelView(main_models.Notification, category='main'))
    admin.add_view(GeneralModelView(main_models.NotificationActivity, category='main'))

    admin.add_view(GeneralModelView(oauth2_models.Client, category='oauth', name='Client'))
    admin.add_view(GeneralModelView(oauth2_models.Grant, category='oauth'))
    admin.add_view(GeneralModelView(oauth2_models.Token, category='oauth'))