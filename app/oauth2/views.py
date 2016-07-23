#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, redirect, url_for, render_template
from flask.views import MethodView

from flask_login import login_required, current_user

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SelectField, HiddenField, TextAreaField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, URL, Optional

from werkzeug.security import gen_salt

from . import models
from JuneMessage import oauth
from accounts.views import get_current_user

class ApplicationsForm(Form):
    name = StringField()
    description = TextAreaField()
    client_id = StringField()
    client_secret = StringField()
    is_confidential = BooleanField('Is Confidential')
    redirect_url = StringField()

class ApplicationsView(MethodView):
    decorators = [login_required]
    template_name = 'oauth/applications.html'

    def get(self):
        clients = models.Client.objects(user=get_current_user())
        return render_template(self.template_name, clients=clients)

class NewApplicationView(MethodView):
    decorators = [login_required]
    template_name = 'oauth/new_application.html'

    def get(self, form=None):
        data = {}
        client_id = gen_salt(40)
        client_secret = gen_salt(50)

        if not form:
            form = ApplicationsForm(client_id=client_id, client_secret=client_secret)

        data['client_id'] = client_id
        data['client_secret'] = client_secret
        data['form'] = form

        return render_template(self.template_name, **data)

    def post(self):
        form = ApplicationsForm(obj=request.form)
        if not form.validate():
            return self.get(form=form)

        client = models.Client()
        client.name = form.name.data.strip()
        client.description = form.description.data.strip()
        client.client_id = form.client_id.data.strip()
        client.client_secret = form.client_secret.data.strip()
        client.user = get_current_user()
        client.is_confidential = form.is_confidential.data
        client._redirect_uris = form.redirect_url.data.strip()
        client._default_scopes = 'read write'

        client.save()

        url = url_for('oauth.applications')
        return redirect(url)

class ApplicationDetailView(MethodView):
    decorators = [login_required]

    template_name = 'oauth/application_detail.html'

    def get(self, client_id):
        client = models.Client.objects(client_id=client_id).first()
        if not client:
            return 'No client found', 404

        data = {'client': client}
        return render_template(self.template_name, **data)


@login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        return render_template('oauthorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'

# @app.route('/oauth/token')
@oauth.token_handler
def access_token():
    return None

# @app.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token(): pass



