#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from JuneMessage import db, oauth
from accounts.models import User
from accounts.views import get_current_user

class Client(db.Document):
    # human readable name, not required
    name = db.StringField()

    # human readable description, not required
    description = db.StringField()

    # creator of the client, not required
    # user_id = db.StringField()
    # required if you need to support client credential
    user = db.ReferenceField(User)

    client_id = db.StringField(primary_key=True)
    client_secret = db.StringField(unique=True, required=True)

    # public or confidential
    is_confidential = db.BooleanField()

    _redirect_uris = db.StringField()
    _default_scopes = db.StringField()

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(db.Document):
    user_id = db.StringField()
    user = db.ReferenceField(User)

    # client_id = db.Column(
    #     db.String(40), db.ForeignKey('client.client_id'),
    #     nullable=False,
    # )
    client_id = db.StringField()
    client = db.ReferenceField(Client)

    code = db.StringField(required=True)

    redirect_uri = db.StringField()
    expires = db.DateTimeField()

    _scopes = db.StringField()

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Document):
    # client_id = db.Column(
    #     db.String(40), db.ForeignKey('client.client_id'),
    #     nullable=False,
    # )
    # client = db.relationship('Client')

    # user_id = db.Column(
    #     db.Integer, db.ForeignKey('user.id')
    # )
    # user = db.relationship('User')

    client_id = db.StringField()
    client = db.ReferenceField(Client)
    user = db.ReferenceField(User)

    # currently only bearer is supported
    token_type = db.StringField()

    access_token = db.StringField(unique=True)
    refresh_token = db.StringField(unique=True)
    expires = db.DateTimeField()
    _scopes = db.StringField()

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


@oauth.clientgetter
def load_client(client_id):
    try:
        return Client.objects.get(client_id=client_id)
    except Client.DoesNotExist:
        return None

@oauth.grantgetter
def load_grant(client_id, code):
    try:
        return Grant.objects.get(client_id=client_id, code=code)
    except Grant.DoesNotExist:
        return None

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=get_current_user(),
        expires=expires
    )
    grant.save()
    return grant

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        try:
            return Token.objects.get(access_token=access_token)
        except Token.DoesNotExist:
            return None
    elif refresh_token:
        try:
            return Token.objects.get(refresh_token=refresh_token)
        except Token.DoesNotExist:
            return None


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    # toks = Token.query.filter_by(client_id=request.client.client_id,
    #                              user_id=request.user.id)
    toks = Token.objects(client_id=request.client.client_id, user_id=request.user.id)
    # make sure that every client has only one token connected to a user
    for t in toks:
        # db.session.delete(t)
        t.delete()

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user=request.user,
    )
    # db.session.add(tok)
    # db.session.commit()
    tok.save()
    return tok