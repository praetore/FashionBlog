import os

__author__ = 'darryl'

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'just-for-testing'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class Testing(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('..', 'test.db')
    LOG_FILE = os.path.abspath(os.path.join(basedir, 'logs', 'log.txt'))

    try:
        import aws_config

        AWS_ACCESS_KEY = aws_config.AWS_ACCESS_KEY
        AWS_SECRET_KEY = aws_config.AWS_SECRET_KEY
        AWS_BUCKET_NAME = aws_config.AWS_BUCKET_NAME
    except ImportError:
        pass


class Production(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join('..', 'test.db')
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')