from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class CharacterSheetForm(FlaskForm):
    name = StringField()
    image = FileField()

class CharacterClassForm(FlaskForm):
    character_class = SelectField()