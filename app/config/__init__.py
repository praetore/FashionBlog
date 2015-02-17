import os

__author__ = 'darryl'

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'just-for-testing'
    DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR') or \
               os.path.join(os.path.dirname(__file__), '..', '..')
    UPLOAD_FOLDER = os.path.abspath(os.path.join(DATA_DIR, 'uploads'))
    LOG_FILE = os.path.abspath(os.path.join(DATA_DIR, 'logs', 'log.txt'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class Testing(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('..', 'test.db')


class Production(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') or \
                              'sqlite:///' + os.path.join('..', 'test.db')