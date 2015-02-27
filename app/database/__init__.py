from app import db
from app.models import Post, Author

__author__ = 'darryl'


def post_create_db(session=None, form=None, image=None):
    description = form.description.data
    email = session.get('email')
    author = Author.query.filter_by(email=email).first()
    post = Post(description=description, author=author, image=image)
    db.session.add(post)
    db.session.commit()


def author_create_db(name, password, email):
    author = Author(name, password, email)
    db.session.add(author)
    db.session.commit()
    return author