import os

__author__ = 'darryl'


class Testing(object):
    SECRET_KEY = 'just-for-testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'log.txt'))


class Production(object):
    pass