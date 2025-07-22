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
        "starting_equipment": "Machado grande, 4 machados, pacote de explorador e 15 PO ou 75 PO."
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
        "starting_equipment": "Cajado ou uma adaga, grimório, pacote de estudioso ou pacote de explorador."
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
        "starting_equipment": "Rapieira ou espada curta, arco curto e aljava com 20 flechas ou uma espada curta, pacote de ladino, pacote de masmorra ou  pacote de explorador, armadura de couro, duas adagas e ferramentas de ladrão."
    },
    {
        "name": "Bardo",
        "icon": "fas fa-harp",
        "description": "",
        "primary_ability": "Carisma",
        "hit_point_die": "d8",
        "saving_throw_proficiencies": "Destreza, Carisma",
        "skill_proficiencies": "Escolha quaisquer 3 perícias",
        "weapon_proficiencies": "Armas simples",
        "tool_proficiencies": "Escolha 3 instrumentos musicais",
        "armor_training": "Armaduras leves",
        "starting_equipament": "Armadura de couro, 2 cdagas, instrumento musical de sua escolha, kit do artista e 19 PO; ou 90 PO"
    },
    {
        "name": "Clérigo",
        "icon": "fas fa-morningstar",
        "description": "",
        "primary_ability": "Sabedoria",
        "hit_point_die": "d8",
        "saving_throw_proficiencies": "Sabedoria, Carisma",
        "skill_proficiencies": "Escolha duas entre: História, Intuição, Medicina, Persuasão, Religião",
        "weapon_proficiencies": "Armas simples",
        "tool_proficiencies": "Nenhuma",
        "armor_training": "Armaduras leves, armaduras médias, escudos",
        "starting_equipament": "Camisão de malha, escudo, maça, símbolo sagrado, pacote de sacerdote e 7 PO; ou 110 PO"
    },
    {
        "name": "Druida",
        "icon": "fas fa-bear",
        "description": "",
        "primary_ability": "Sabedoria",
        "hit_point_die": "d8",
        "saving_throw_proficiencies": "Inteligência, Sabedoria",
        "skill_proficiencies": "Escolha duas entre: Arcanismo, Lidar com Animais, Intuição, Medicina, Natureza, Persuasão, Religião, Sobrevivência",
        "weapon_proficiencies": "Armas simples",
        "tool_proficiencies": "Kit de herbalismo",
        "armor_training": "Armaduras leves, escudos",
        "starting_equipament": "Armadura de couro, escudo, foice, foco druídico(cajado), pacote de explorador, kit de herbalismo e 9 PO; ou 50 PO"
    },
    {
        "name": "Guerreiro",
        "icon": "fas fa-sword",
        "description": "",
        "primary_ability": "Força ou Destreza",
        "hit_point_die": "d10",
        "saving_throw_proficiencies": "Força, Constituição",
        "skill_proficiencies": "Escolha duas entre: Acrobacia, Lidar com Animais, Atletismo, História, Intuição, Intimidação, Persuasão, Percepção, Sobrevivência",
        "weapon_proficiencies": "Armas simples, armas marciais",
        "tool_proficiencies": "Nenhuma",
        "armor_training": "Armaduras leves, armaduras médias, armaduras pesadas, escudos",
        "starting_equipament": "Camisão de malha, espada grande, mangual, 8 javelins, pacote de masmorra / Armadura de couro batido, cimitarra, espda curta, arco longo, aljava com 20 flechas, pacote de masmorra e 11 PO; ou 155 PO"
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
