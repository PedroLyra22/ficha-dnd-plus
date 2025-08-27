import enum
from email.policy import default
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import CheckConstraint

from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def repr(self):
        return f"User('{self.nome}', '{self.email}')"

class AdvancementType(enum.Enum):
    MILESTONE = 'MILESTONE'
    XP = 'XP'

class HitPointType(enum.Enum):
    FIXO = 'FIXO'
    MANUAL = 'MANUAL'

class ConfigSheet(db.Model):
    __tablename__ = 'config_sheets'
    id = db.Column(db.Integer, primary_key=True)
    homebrew = db.Column(db.Boolean, nullable=False, default=False)
    expanded_rules = db.Column(db.Boolean, nullable=False, default=False)
    dice_rolling = db.Column(db.Boolean, nullable=False, default=False)
    advancement_type = db.Column(db.Enum(AdvancementType), nullable=False, default=AdvancementType.MILESTONE)
    hit_point_type = db.Column(db.Enum(HitPointType), nullable=False, default=HitPointType.MANUAL)
    feat_prerequisites = db.Column(db.Boolean, nullable=False, default=False)
    multiclass_prerequisites = db.Column(db.Boolean, nullable=False, default=False)
    mark_level_scaled_spells = db.Column(db.Boolean, nullable=False, default=False)

class ClassType(db.Model):
    __tablename__ = 'class_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    icon = db.Column(db.String)
    description = db.Column(db.Text)
    #features = db.Column(JSONB)

class CharacterSheet(db.Model):
    __tablename__ = 'character_sheets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.Text)
    mimetype = db.Column(db.String(50))
    level = db.Column(db.Integer, nullable=False)
    proficiency_bonus = db.Column(db.Integer, default=2)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    config_sheet_id = db.Column(db.Integer, db.ForeignKey('config_sheets.id'), nullable=False)
    class_type_id = db.Column(db.Integer, db.ForeignKey('class_types.id'), nullable=False)
    user = db.relationship('User', backref='character_sheets', lazy=True)
    config_sheet = db.relationship('ConfigSheet', backref='character_sheets', lazy=True)
    class_type = db.relationship('ClassType', backref='character_sheets', lazy=True)
    attributes = db.relationship('CharacterSheetAttribute', backref='character_sheet', uselist=False)
    skills = db.relationship('CharacterSheetSkill', backref='character_sheet_skill', uselist=False)

class SubclassType(db.Model):
    __tablename__ = 'subclass_types'
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.Text)

class ClassFeature(db.Model):
    __tablename__ = 'class_features'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    level = db.Column(db.Text)
    description = db.Column(db.Text)
    #choices = db.Column(JSONB)

class CharacterSheetAttribute(db.Model):
    __tablename__ = 'character_sheet_attributes'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.Integer, nullable=False, default=10)
    dexterity = db.Column(db.Integer, nullable=False, default=10)
    constitution = db.Column(db.Integer, nullable=False, default=10)
    intelligence = db.Column(db.Integer, nullable=False, default=10)
    wisdom = db.Column(db.Integer, nullable=False, default=10)
    charisma = db.Column(db.Integer, nullable=False, default=10)
    character_sheet_id = db.Column(db.Integer, db.ForeignKey('character_sheets.id'), unique=True, nullable=False)


class CharacterSheetSkill(db.Model):
    __tablename__ = 'character_sheet_skills'
    id = db.Column(db.Integer, primary_key=True)
    character_sheet_id = db.Column(db.Integer, db.ForeignKey('character_sheets.id'), unique=True, nullable=False)
    acrobatics = db.Column(db.Integer, default=0)
    animal_handling = db.Column(db.Integer, default=0)
    arcana = db.Column(db.Integer, default=0)
    athletics = db.Column(db.Integer, default=0)
    deception = db.Column(db.Integer, default=0)
    history = db.Column(db.Integer, default=0)
    insight = db.Column(db.Integer, default=0)
    intimidation = db.Column(db.Integer, default=0)
    investigation = db.Column(db.Integer, default=0)
    medicine = db.Column(db.Integer, default=0)
    nature = db.Column(db.Integer, default=0)
    perception = db.Column(db.Integer, default=0)
    performance = db.Column(db.Integer, default=0)
    persuasion = db.Column(db.Integer, default=0)
    religion = db.Column(db.Integer, default=0)
    sleight_of_hand = db.Column(db.Integer, default=0)
    stealth = db.Column(db.Integer, default=0)
    survival = db.Column(db.Integer, default=0)


weapon_properties = db.Table(
    'weapon_properties',
    db.Column('weapon_id', db.Integer, db.ForeignKey('weapons.id'), primary_key=True),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'), primary_key=True)
)

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    weapons = db.relationship(
        'Weapon',
        secondary=weapon_properties,
        back_populates='properties'
    )

class Weapon(db.Model):
    __tablename__ = 'weapons'

    id = db.Column(db.Integer, primary_key=True)
    weapon_type = db.Column(db.String(80))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    damage = db.Column(db.String(20))
    damage_type = db.Column(db.String(50))
    weight = db.Column(db.String(20))
    cost = db.Column(db.String(20))

    mastery_id = db.Column(db.Integer, db.ForeignKey('masteries.id'), nullable=True)
    mastery = db.relationship('Mastery', back_populates='weapons')

    properties = db.relationship(
        'Property',
        secondary=weapon_properties,
        back_populates='weapons'
    )

class Mastery(db.Model):
    __tablename__ = 'masteries'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    weapons = db.relationship('Weapon', back_populates='mastery')