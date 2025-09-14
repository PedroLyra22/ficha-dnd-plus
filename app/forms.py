from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class CharacterSheetForm(FlaskForm):
    name = StringField('Nome do Personagem', validators=[DataRequired()])
    class_slug = SelectField('Classe', validators=[DataRequired()])
    submit = SubmitField('Criar Personagem')
