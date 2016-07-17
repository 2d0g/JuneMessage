#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

from . import views

oauth = Blueprint('oauth', __name__)

oauth.add_url_rule('/view/applications/', view_func=views.ApplicationsView.as_view('oauth_applications'))