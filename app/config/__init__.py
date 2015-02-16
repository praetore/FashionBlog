__author__ = 'darryl'


class Testing(object):
    SECRET_KEY = 'just-for-testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class Production(object):
    pass