from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

class CharacterSheetForm(FlaskForm):
    name = StringField()
    image = FileField()

class CharacterClassForm(FlaskForm):
    character_class = SelectField('Classe', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Selecionar')

class ClassFeatureForm(FlaskForm):
    trait_choices = [
        ('healers_touch', 'Toque do Curandeiro'),
        ('divine_shield', 'Escudo Divino'),
        ('holy_smite', 'Golpe Sagrado')
    ]

    trait = SelectField(
        'Escolha sua Característica',
        choices=trait_choices,
        validators=[DataRequired(message="É necessário selecionar uma característica.")]
    )
    submit = SubmitField('Confirmar Escolha')