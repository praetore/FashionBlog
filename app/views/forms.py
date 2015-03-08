from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf import Form
from wtforms import SubmitField, FileField, StringField, PasswordField, BooleanField, Field
from wtforms.validators import DataRequired, InputRequired, EqualTo
from wtforms.widgets import TextInput

__author__ = 'darryl'


class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []


class CreatePostForm(Form):
    title = StringField('Titel', validators=[InputRequired()])
    content = PageDownField("Inhoud "
                                "(in <a href=\"https://help.github.com/articles/"
                                "github-flavored-markdown/\">Markdown</a>)",
                                validators=[DataRequired()])
    tags = TagListField('Tags')
    submit = SubmitField('Posten')


class UploadImageForm(Form):
    image = FileField('Selecteer een afbeelding')
    submit = SubmitField('Uploaden')


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