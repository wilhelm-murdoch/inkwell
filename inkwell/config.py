# -*- coding: utf-8 -*-
class Config(object):
    DEBUG = True
    ENVIRONMENT = 'local'
    HOST = '127.0.0.1'
    PORT = 9001
    TESTING = False
    CACHE_TTL = 28800
    ARTICLES_FOLDER = 'articles'

class LocalConfig(Config):
    pass

class TestConfig(Config):
    TESTING = True
    ENVIRONMENT = 'testing'
    ARTICLES_FOLDER = 'tests/articles/valid'

class ProductionConfig(Config):
    DEBUG = False
    ENVIRONMENT = 'production'
