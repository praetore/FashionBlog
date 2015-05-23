from datetime import datetime

from flask.ext.login import UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


__author__ = 'darryl'

taglist = db.Table('taglists',
                   db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                   db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.relationship('Tag',
                           secondary=taglist,
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')
    author_id = db.Column(db.Integer, ForeignKey('authors.id'))

    def __init__(self, title=None, author=None, content=None):
        self.title = title
        self.author_id = author.id
        self.content = content


class Author(db.Model, UserMixin):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    pwdhash = db.Column(db.String, nullable=False)

    def __init__(self, name, password, email):
        self.name = name
        self.pwdhash = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name