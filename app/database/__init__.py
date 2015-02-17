from app import db
from app.models import Post, Author

__author__ = 'darryl'


def post_create_db(form=None, image=None):
    description = form.description.data
    name = form.author.data
    author = Author.query.filter_by(name=name).first()
    if not author:
        author = author_create_db(name)
    post = Post(description=description, author=author, image=image)
    db.session.add(post)
    db.session.commit()


def author_create_db(name):
    author = Author(name)
    db.session.add(author)
    db.session.commit()
    return author