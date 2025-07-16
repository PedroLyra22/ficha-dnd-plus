import enum

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

class CharacterSheet(db.Model):
    __tablename__ = 'character_sheets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.Text)
    mimetype = db.Column(db.String(50))

class ClassType(db.Model):
    __tablename__ = 'class_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)
    description = db.Column(db.Text)
    primary_ability = db.Column(db.String)
    hit_point_die = db.Column(db.String)
    saving_throw_proficiencies = db.Column(db.String)
    skill_proficiencies = db.Column(db.Text)
    weapon_proficiencies = db.Column(db.String)
    tool_proficiencies = db.Column(db.String)
    armor_training = db.Column(db.String)
    starting_equipment = db.Column(db.Text)

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


