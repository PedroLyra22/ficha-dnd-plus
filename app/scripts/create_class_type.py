import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import ClassType

from app import create_app

app = create_app()

classes_data = [
    {
        "name": "Bárbaro",
        "icon": "fas fa-axe",
        "description": "Um guerreiro feroz de origem primitiva que pode entrar em fúria em combate.",
        "primary_ability": "Força",
        "hit_point_die": "d12",
        "saving_throw_proficiencies": "Força, Constituição",
        "skill_proficiencies": "Escolha duas entre: Atletismo, Intimidação, Natureza, Percepção, Sobrevivência",
        "weapon_proficiencies": "Armas simples, armas marciais",
        "tool_proficiencies": "Nenhuma",
        "armor_training": "Armaduras leves, armaduras médias, escudos",
        "starting_equipment": "Um machado grande ou qualquer arma marcial corpo a corpo, um machado de mão ou qualquer arma simples, um pacote de explorador e quatro azagaias."
    },
    {
        "name": "Mago",
        "icon": "fas fa-book-sparkles",
        "description": "Um usuário de magia erudito capaz de manipular as estruturas da realidade.",
        "primary_ability": "Inteligência",
        "hit_point_die": "d6",
        "saving_throw_proficiencies": "Inteligência, Sabedoria",
        "skill_proficiencies": "Escolha duas entre: Arcanismo, História, Investigação, Medicina, Intuição",
        "weapon_proficiencies": "Adagas, dardos, fundas, cajados, bestas leves",
        "tool_proficiencies": "Nenhuma",
        "armor_training": "Nenhuma",
        "starting_equipment": "Um cajado ou uma adaga, um grimório, um pacote de estudioso ou um pacote de explorador."
    },
    {
        "name": "Ladino",
        "icon": "fas fa-dagger",
        "description": "Um batedor, ladrão ou espião que prospera nas sombras.",
        "primary_ability": "Destreza",
        "hit_point_die": "d8",
        "saving_throw_proficiencies": "Destreza, Inteligência",
        "skill_proficiencies": "Escolha quatro entre: Acrobacia, Atletismo, Enganação, Intuição, Intimidação, Investigação, Percepção, Performance, Persuasão, Prestidigitação, Furtividade",
        "weapon_proficiencies": "Armas simples, bestas de mão, espadas longas, rapieiras, espadas curtas",
        "tool_proficiencies": "Ferramentas de ladrão",
        "armor_training": "Armaduras leves",
        "starting_equipment": "Uma rapieira ou uma espada curta, um arco curto e aljava com 20 flechas ou uma espada curta, um pacote de assaltante, um pacote de masmorra ou um pacote de explorador, armadura de couro, duas adagas e ferramentas de ladrão."
    }
]


def populate_database(classes_data):
    with app.app_context():
        db.create_all()
        for class_data in classes_data:
            # existing_class = ClassType.query.filter_by(name=classes_data['name']).first()
            # if not existing_class:
            new_class = ClassType(**class_data)
            db.session.add(new_class)
            print(f"Adicionando classe: {class_data['name']}")
        db.session.commit()


if __name__ == '__main__':
    populate_database(classes_data)
