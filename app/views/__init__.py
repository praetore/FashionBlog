import os
from flask import render_template, request, flash, url_for, redirect, g, send_from_directory
from flask.ext.login import login_required, current_user, login_user, logout_user
from app import app, Post, post_create_db, login_manager
from app.database import author_create_db, post_remove_db
from app.handlers import LocalStorage, S3Storage
from app.models import Author, Tag
from app.views.forms import CreatePostForm, LoginForm, RegistrationForm, UploadImageForm

__author__ = 'darryl'

if app.config["TESTING"]:
    handler = LocalStorage()
else:
    handler = S3Storage()


@login_manager.user_loader
def load_user(user_id):
    return Author.query.get(int(user_id))


@app.before_request
def get_current_user():
    g.user = current_user


@app.route('/')
def index():
    posts = Post.query.all()
    count = Post.query.count()
    return render_template('index.html', posts=posts, count=count)


@app.route('/<tag>')
def posts_by_tag(tag):
    posts = Post.query.join(Post.tags).filter(Tag.name.in_([tag])).all()
    count = Post.query.join(Post.tags).filter(Tag.name.in_([tag])).count()
    return render_template('index.html', posts=posts, count=count)


@app.route('/post-list')
@login_required
def post_list():
    author = Author.query.get(current_user.id)
    posts = Post.query.filter_by(author=author).all()
    return render_template('post-overview.html', posts=posts)


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm(request.form)
    if form.validate_on_submit():
        post_create_db(author_id=current_user.id, form=form)
        app.logger.info('Post created')
        flash("Post aangemaakt", 'success')
        return redirect(url_for('post_list'))
    return render_template('dashboard-component.html', form=form, form_action='create_post')


@app.route('/remove-post/<int:post_id>')
@login_required
def remove_post(post_id):
    post_remove_db(post_id)
    return redirect(url_for('post_list'))


@app.route('/remove-image/<filename>')
@login_required
def remove_image(filename):
    handler.delete_image(filename)
    return redirect(url_for('image_list'))


@app.route('/list-images', methods=['POST', 'GET'])
@login_required
def image_list():
    form = UploadImageForm(request.form)
    if form.validate_on_submit():
        image = request.files['image']
        app.logger.info('Processing %s' % image.filename)
        handler.store_image(image)
    s3_images = handler.list_images()
    return render_template('image-upload.html', form=form, images=s3_images)


@app.route('/images/<filename>')
def get_images(filename):
    if app.config["TESTING"]:
        return send_from_directory(app.config["STORAGE_DIRECTORY"], filename)
    return redirect(handler.get_image(filename))


@app.route('/img/<path:path>')
def images(path):
    return app.send_static_file(os.path.join('img', path).replace('\\', '/'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        flash('Je bent al ingelogd.', 'info')
        return redirect(url_for('create_post'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = Author.query.filter_by(email=email).first()
        if not existing_user:
            flash('Deze gebruiker bestaat niet', 'danger')
            return render_template('dashboard-component.html', form=form, form_action='login')
        if not existing_user.check_password(password):
            flash('Foutief wachtwoord ingevoerd', 'danger')
            return render_template('dashboard-component.html', form=form, form_action='login')

        login_user(existing_user)
        flash('Je bent nu ingelogd.', 'success')
        return redirect(url_for('post_list'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('dashboard-component.html', form=form, form_action='login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_username = Author.query.filter_by(email=email).first()

        if existing_username:
            flash(
                'Er is al een account geregistreerd onder dit e-mailadres.',
                'warning'
            )
            return render_template('dashboard-component.html', form=form, form_action='register')

        new_user = author_create_db(name, password, email)
        app.logger.info("Account %s created" % new_user.name)
        flash('Account aangemaakt. Je kunt nu inloggen', 'success')
        return redirect(url_for('login'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('dashboard-component.html', form=form, form_action='register')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd', 'success')
    return redirect(url_for('index'))