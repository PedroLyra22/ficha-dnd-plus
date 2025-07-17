from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired

class CharacterSheetForm(FlaskForm):
    name = StringField()
    image = FileField()

class CharacterClassForm(FlaskForm):
    character_class = SelectField('Classe', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Selecionar')