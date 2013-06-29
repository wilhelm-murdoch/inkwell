# -*- coding: utf-8 -*-
class Config(object):
    DEBUG = True
    ENVIRONMENT = 'local'
    HOST = '127.0.0.1'
    PORT = 9001
    TESTING = False
    TEMPLATE_FOLDER = None
    STATIC_FOLDER = None
    STATIC_URL_PATH = None
    ARTICLES_FOLDER = None

class LocalConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
    ENVIRONMENT = 'testing'

class ProductionConfig(Config):
    DEBUG = False
    ENVIRONMENT = 'production'
