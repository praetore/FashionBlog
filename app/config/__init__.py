import os

__author__ = 'darryl'

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..')


class Config(object):
    SECRET_KEY = os.environ.get('OPENSHIFT_SECRET_TOKEN') or 'just-for-testing'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class Testing(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    STORAGE_DIRECTORY = os.path.abspath(os.path.join(basedir, 'storage'))
    LOG_FILE = os.path.join(STORAGE_DIRECTORY, 'log.txt')


class Production(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL')
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')