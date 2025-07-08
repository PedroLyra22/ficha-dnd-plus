import enum

from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def repr(self):
        return f"User('{self.nome}', '{self.email}')"

class CharacterSheet(db.Model):
    __tablename__ = 'character_sheets'
    id = db.Column(db.Integer, primary_key=True)

class AdvancementType(enum.Enum):
    MILESTONE = 'Milestone'
    EXPERIENCE = 'XP'

class SheetConfig(db.Model):
    __tablename__ = 'sheet_configs'
    id = db.Column(db.Integer, primary_key=True)
    homebrew = db.Column(db.Boolean, nullable=False, default=False)
    expanded_rules = db.Column(db.Boolean, nullable=False, default=False)
    dice_rolling = db.Column(db.Boolean, nullable=False, default=False)
    advancement_type = db.Column(db.Enum(AdvancementType), nullable=False, default=AdvancementType.MILESTONE)
