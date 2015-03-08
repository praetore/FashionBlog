from app import db, app
from app.models import Post, Author, Tag

__author__ = 'darryl'


def post_create_db(author_id=None, form=None):
    content = form.content.data
    title = form.title.data
    tags = form.tags.data
    author = Author.query.get(author_id)
    post = Post(content=content, author=author, title=title)
    for t in tags:
        tag = Tag(t)
        post.tags.append(tag)
    db.session.add(post)
    db.session.commit()


def author_create_db(name=None, password=None, email=None):
    author = Author(name=name, password=password, email=email)
    db.session.add(author)
    db.session.commit()
    return author


def post_remove_db(post_id=None):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()