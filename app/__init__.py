import os
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from app.views.forms import CreatePost

__author__ = 'darryl'

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

try:
    current_env = os.environ['CURRENT_ENV']
except KeyError:
    current_env = 'Testing'

current_env = 'app.config.' + current_env
app.config.from_object(current_env)

db = SQLAlchemy(app)

from app.models import Post
from app.database import create_post


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CreatePost()
    if form.validate_on_submit():
        create_post(form)
        form.content.data = ''
        form.author.data = ''
    posts = Post.query.all()
    count = Post.query.count()
    return render_template('index.html', posts=posts, form=form, count=count)

db.create_all()
