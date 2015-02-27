import os
from flask import render_template, request, flash, url_for, redirect, session
from flask.ext.login import login_required
from app import app, Post, post_create_db
from app.database import author_create_db
from app.handlers import store_image, get_image
from app.models import Author
from app.views.forms import CreatePostForm, LoginForm, RegistrationForm

__author__ = 'darryl'


@app.route('/')
def index():
    posts = Post.query.all()
    count = Post.query.count()
    return render_template('index.html', posts=posts, count=count)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
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
        flash("Post aangemaakt", 'success')
        return redirect(url_for('index'))
    return render_template('create-post.html', form=form)


@app.route('/images/<filename>')
def get_images(filename):
    return redirect(get_image(filename))


@app.route('/img/<path:path>')
def images(path):
    return app.send_static_file(os.path.join('img', path).replace('\\', '/'))


@app.route('/login')
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = Author.filter_by(email=email).first()
        if not existing_user:
            flash('Gebruiker bestaat niet', 'danger')
            return render_template('login.html', form=form)
        if not existing_user.check_password(password):
            flash('Foutief wachtwoord', 'danger')
            return render_template('login.html', form=form)

        session['email'] = email
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        flash('Your are already logged in.', 'info')
        return redirect(url_for('auth.home'))
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
            return render_template('register.html', form=form)
        author_create_db(name, password, email)
        flash('Account aangemaakt. Je kunt nu inloggen', 'success')
        return redirect(url_for('index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    if 'username' in session:
        session.pop('email')
        flash('Je bent nu uitgelogd.', 'success')
    return redirect(url_for('auth.home'))