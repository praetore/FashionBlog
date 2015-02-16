from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

__author__ = 'darryl'


class CreatePost(Form):
    content = StringField("Wat wil je zeggen?", validators=[DataRequired()])
    author = StringField('Je naam', validators=[DataRequired()])
    submit = SubmitField('Post')