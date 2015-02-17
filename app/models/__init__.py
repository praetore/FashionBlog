from datetime import datetime
import bleach
from markdown import markdown
from sqlalchemy import ForeignKey
from app import db

__author__ = 'darryl'


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('authors.id'))
    image = db.Column(db.String, nullable=False)

    def __init__(self, author=None, description=None, image=None):
        self.author_id = author.id
        self.image = image
        self.description = self.parse(description)

    @classmethod
    def parse(cls, value):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        return bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    name = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, name):
        self.name = name