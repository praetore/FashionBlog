import os
from flask import render_template, request, flash, url_for, redirect, g
from flask.ext.login import login_required, current_user, login_user, logout_user
from app import app, Post, post_create_db, login_manager
from app.database import author_create_db
from app.handlers import store_image, get_image
from app.models import Author
from app.views.forms import CreatePostForm, LoginForm, RegistrationForm

__author__ = 'darryl'


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
    return render_template('post-list.html', posts=posts, count=count)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = CreatePostForm(request.form)
    if form.validate_on_submit():
        app.logger.info('Using bucket for image store')
        file = request.files['image']
        app.logger.info('Processing ' + file.filename)
        store_image(file)
        app.logger.info('Image stored in bucket')
        post_create_db(author_id=current_user.id, form=form, image=file.filename)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        flash('Je bent al ingelogd.', 'info')
        return redirect(url_for('dashboard'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = Author.query.filter_by(email=email).first()
        if not existing_user:
            flash('Deze gebruiker bestaat niet', 'danger')
            return render_template('form-display.html', form=form, form_action='login')
        if not existing_user.check_password(password):
            flash('Foutief wachtwoord ingevoerd', 'danger')
            return render_template('form-display.html', form=form, form_action='login')

        login_user(existing_user)
        flash('Je bent nu ingelogd.', 'success')
        return redirect(url_for('dashboard'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('form-display.html', form=form)


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
            return render_template('form-display.html', form=form, form_action='register')

        new_user = author_create_db(name, password, email)
        app.logger.info(new_user.name)
        flash('Account aangemaakt. Je kunt nu inloggen', 'success')
        return redirect(url_for('index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('form-display.html', form=form, form_action='register')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd', 'success')
    return redirect(url_for('index'))