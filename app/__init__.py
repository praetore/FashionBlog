import os

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.markdown import Markdown
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.sqlalchemy import SQLAlchemy

from app.config import basedir


__author__ = 'darryl'

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
pagedown = PageDown(app)
md = Markdown(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

current_env = 'app.config.{}'.format(os.environ.get('CURRENT_ENV', 'Testing'))
app.config.from_object(current_env)

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

if app.debug:
    directory = app.config["STORAGE_DIRECTORY"]
    if not os.path.exists(directory):
        os.makedirs(directory)

    import logging
    from logging import FileHandler

    file_handler = FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

from app.models import Post, Author
from app.database import post_create_db
from app.views import login_manager, app

db.create_all()

if __name__ == '__main__':
    app.run()