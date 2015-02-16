from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

__author__ = 'darryl'


class CreatePostForm(Form):
    author = StringField('Auteur', validators=[DataRequired()])
    title = StringField('Titel', validators=[DataRequired()])
    content = StringField("Beschrijving", validators=[DataRequired()])
    submit = SubmitField('Post')