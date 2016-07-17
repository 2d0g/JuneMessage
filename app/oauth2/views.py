#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, render_template
from flask.views import MethodView

from flask_login import login_required, current_user

from . import models
from accounts.views import get_current_user

class ApplicationsView(MethodView):
    template_name = 'oauth/applications.html'

    def get(self):
        clients = models.Client.objects(user=get_current_user())

        return render_template(self.template_name, clients=clients)
