import os
from flask import render_template, request, flash, url_for, redirect, send_from_directory
from app import app, Post, upload_file, post_create_db
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
    if request.method == 'POST':
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