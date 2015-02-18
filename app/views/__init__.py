import os
from flask import render_template, request, flash, url_for, redirect
from app import app, Post, post_create_db
from app.handlers import store_image, get_image
from app.views.forms import CreatePostForm

__author__ = 'darryl'


@app.route('/')
def index():
    posts = Post.query.all()
    count = Post.query.count()
    return render_template('index.html', posts=posts, count=count)


@app.route('/dashboard', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm(request.form)
    if form.validate_on_submit():
        app.logger.info('Using bucket for image store')
        file = request.files['image']
        app.logger.info('Processing ' + file.filename)
        store_image(file)
        app.logger.info('Image stored in bucket')
        post_create_db(form, file.filename)
        app.logger.info('Post created')
        flash("Post aangemaakt")
        return redirect(url_for('index'))
    return render_template('create-post.html', form=form)


@app.route('/images/<filename>')
def get_images(filename):
    return redirect(get_image(filename))


@app.route('/img/<path:path>')
def images(path):
    return app.send_static_file(os.path.join('img', path).replace('\\', '/'))