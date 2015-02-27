import os
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.sqlalchemy import SQLAlchemy
from app.config import basedir

__author__ = 'darryl'

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
pagedown = PageDown(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

try:
    current_env = os.environ['CURRENT_ENV']
except KeyError:
    current_env = 'Testing'

current_env = 'app.config.' + current_env
app.config.from_object(current_env)

if app.config['DEBUG']:
    directory = os.path.abspath(os.path.join(basedir, 'logs'))
    if not os.path.exists(directory):
        os.makedirs(directory)

    import logging
    from logging import FileHandler

    file_handler = FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

from app.models import Post, Author
from app.database import post_create_db

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Author.query.get(int(user_id))

from app.views import app

db.drop_all()
db.create_all()