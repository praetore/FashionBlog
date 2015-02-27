from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf import Form
from wtforms import SubmitField, FileField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, EqualTo

__author__ = 'darryl'


class CreatePostForm(Form):
    description = PageDownField("Beschrijving (in Markdown)", validators=[DataRequired()])
    image = FileField('Selecteer een afbeelding')
    submit = SubmitField('Posten')


class RegistrationForm(Form):
    name = StringField('Naam', validators=[InputRequired()])
    email = StringField('E-mailadres', validators=[InputRequired()])
    password = PasswordField('Wachtwoord',
                             validators=[InputRequired(), EqualTo('confirm', 'Wachtwoorden moeten overeenkomen')])
    confirm = PasswordField('Wachtwoord bevestigen', validators=[InputRequired()])
    submit = SubmitField('Registreren')


class LoginForm(Form):
    email = StringField('E-mailadres', validators=[InputRequired()])
    password = PasswordField('Wachtwoord', validators=[InputRequired()])
    remember_me = BooleanField('Onthoud mij')
    submit = SubmitField('Inloggen')