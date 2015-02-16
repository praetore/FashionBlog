from datetime import datetime
from app import db

__author__ = 'darryl'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)

    def __init__(self, author, content):
        self.author = author
        self.content = content