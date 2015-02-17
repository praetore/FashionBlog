import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.sqlalchemy import SQLAlchemy

from app.views.forms import CreatePostForm


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

import logging
from logging import FileHandler
file_handler = FileHandler(app.config['LOG_FILE'])
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

db = SQLAlchemy(app)

from app.models import Post
from app.handlers import allowed_file, upload_file
from app.database import post_create_db


@app.route('/')
def index():
    posts = Post.query.all()
    count = Post.query.count()
    return render_template('index.html', posts=posts, count=count)


@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm(request.form)
    if request.method == 'POST':
        app.logger.info('POST method called')
        app.logger.info(form.validate_on_submit())
        if form.validate_on_submit():
            filename = upload_file(request)
            post_create_db(form, filename)
            flash("Post aangemaakt")
            return redirect(url_for('index'))
    return render_template('create-post.html', form=form)


@app.route('/images/<filename>')
def retrieve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/img/<path:path>')
def images(path):
    return app.send_static_file(os.path.join('img', path).replace('\\', '/'))


db.create_all()