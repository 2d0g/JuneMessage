#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, render_template
from flask.views import MethodView

from flask_login import login_required, current_user

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SelectField, HiddenField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, URL, Optional

from werkzeug.security import gen_salt

from . import models
from accounts.views import get_current_user

class ApplicationsForm(Form):
    name = StringField()
    description = PasswordField()
    client_id = HiddenField()
    client_secret = HiddenField()
    is_confidential = BooleanField('Is Confidential')

class ApplicationsView(MethodView):
    template_name = 'oauth/applications.html'

    def get(self):
        clients = models.Client.objects(user=get_current_user())
        return render_template(self.template_name, clients=clients)

class NewApplicationView(MethodView):
    template_name = 'oauth/new_application.html'

    def get(self):
        client_id = gen_salt(40),
        client_secret = gen_salt(50)

        form = ApplicationsForm(client_id=client_id, client_secret=client_secret)

        return render_template(self.template_name, form=form)