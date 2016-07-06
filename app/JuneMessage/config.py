#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, logging

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers = {
        'console': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG},
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'JuneMessage.log',
            'formatter': 'f'},
        },
    root = {
        'handlers': ['console', 'file'],
        'level': logging.DEBUG,
        },
)

class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjdljLJfsa(&&^%$DL08_80jflKzcznv*c'
    MONGODB_SETTINGS = {'db': 'JuneMessage'}

    TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates').replace('\\', '/')
    STATIC_PATH = os.path.join(BASE_DIR, 'static').replace('\\', '/')

    # email server
    # MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    # MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'chmod777gevinyu@gmail.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Chmod777@gevinyu'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ALIDAYU_APP_KEY = '23368054'
    ALIDAYU_APP_SECRET = '95cfb0bf8ef66410cae70d120e57d9e3'

    PER_PAGE = 20
    PER_PAGE_MAX = 100


    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True

class PrdConfig(Config):
    # DEBUG = False
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    MONGODB_SETTINGS = {
            'db': 'JuneMessage',
            'host': os.environ.get('MONGO_HOST') or 'localhost',
            # 'port': 12345
        }


config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'default': DevConfig,
}