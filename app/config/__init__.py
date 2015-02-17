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
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['OPENSHIFT_POSTGRESQL_DB_URL']
    DATA_DIR = os.environ['OPENSHIFT_DATA_DIR']
    UPLOAD_FOLDER = os.path.abspath(os.path.join(DATA_DIR, 'uploads'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    LOG_FILE = os.path.abspath(os.path.join(DATA_DIR, 'logs', 'log.txt'))