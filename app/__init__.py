import os
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.sqlalchemy import SQLAlchemy

__author__ = 'darryl'

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
pagedown = PageDown(app)

try:
    current_env = os.environ['CURRENT_ENV']
except KeyError:
    current_env = 'Testing'

current_env = 'app.config.' + current_env
app.config.from_object(current_env)

for directory in [
    app.config['UPLOAD_FOLDER'],
    os.path.abspath(os.path.join(app.config['DATA_DIR'], 'logs'))
]:
    if not os.path.exists(directory):
        os.makedirs(directory)

import logging
from logging import FileHandler
file_handler = FileHandler(app.config['LOG_FILE'])
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

db = SQLAlchemy(app)

from app.models import Post
from app.handlers import allowed_file, upload_file
from app.database import post_create_db

from app.views import app

db.create_all()