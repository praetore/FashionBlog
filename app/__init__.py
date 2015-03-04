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

current_env = os.environ.get('CURRENT_ENV') or 'Testing'
current_env = 'app.config.' + current_env
app.config.from_object(current_env)

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

if app.debug:
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
from app.views import login_manager

from app.views import app

db.create_all()