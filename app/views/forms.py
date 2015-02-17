from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf import Form
from wtforms import SubmitField, FileField, SelectField
from wtforms.validators import DataRequired

__author__ = 'darryl'


class CreatePostForm(Form):
    description = PageDownField("Beschrijving (in Markdown)", validators=[DataRequired()])
    author = SelectField('Auteur', validators=[DataRequired()], choices=[
        ('Anouk', 'Anouk'),
        ('Darryl', 'Darryl'),
        ('Junior', 'Junior'),
        ('Rolf', 'Rolf')
    ])
    image = FileField('Selecteer een afbeelding')
    submit = SubmitField('Posten')