import os

__author__ = 'darryl'


class Testing(object):
    SECRET_KEY = 'just-for-testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('..', 'test.db')
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..')
    UPLOAD_FOLDER = os.path.abspath(os.path.join(DATA_DIR, 'uploads'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    LOG_FILE = os.path.abspath(os.path.join(DATA_DIR, 'logs', 'log.txt'))


class Production(object):
    pass