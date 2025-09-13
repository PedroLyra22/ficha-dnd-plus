from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

class CharacterSheetForm(FlaskForm):
    name = StringField()
    image = FileField()