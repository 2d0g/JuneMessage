#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

from . import views

oauth = Blueprint('oauth', __name__)

oauth.add_url_rule('/view/applications/', view_func=views.ApplicationsView.as_view('applications'))
oauth.add_url_rule('/view/new-application/', view_func=views.NewApplicationView.as_view('new_application'))
oauth.add_url_rule('/view/applications/<client_id>/', view_func=views.ApplicationDetailView.as_view('application_detail'))

oauth.add_url_rule('/authorize', 'authorize', views.authorize, methods=['GET', 'POST'])
oauth.add_url_rule('/token', 'access_token', views.access_token, methods=['GET', 'POST'])
oauth.add_url_rule('/revoke', 'revoke_token', views.revoke_token, methods=['POST'])