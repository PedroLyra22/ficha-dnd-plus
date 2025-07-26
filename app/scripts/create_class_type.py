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
        "icon": "app/static/img/class_icons/icon-barbarian.png",
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
        "icon": "fas fa-book",
        "description": "Um usuário de magia erudito capaz de manipular as estruturas da realidade.",
        "primary_ability": "Inteligência",
        "hit_point_die": "d6",
        "saving_throw_proficiencies": "Inteligência, Sabedoria",
        "skill_proficiencies": "Escolha duas entre: Arcanismo, História, Intuição, Investigação, Medicina, Natureza, Religião",
        "weapon_proficiencies": "Armas simples",
        "tool_proficiencies": "Nenhuma",
        "armor_training": "Nenhuma",
        "starting_equipment": "2 adagas, foco arcano(cajado), robe, livro de magias, pacote de estudioso e 5 PO ou 55 PO"
    },
    {
        "name": "Ladino",
        "icon": "fas fa-dagger",
        "description": "Um batedor, ladrão ou espião que prospera nas sombras.",
        "primary_ability": "Destreza",
        "hit_point_die": "d8",
        "saving_throw_proficiencies": "Destreza, Inteligência",
        "skill_proficiencies": "Escolha quatro entre: Acrobacia, Atletismo, Enganação, Intuição, Intimidação, Investigação, Percepção, Persuasão, Prestidigitação, Furtividade",
        "weapon_proficiencies": "Armas simples, armas marciais com propriedades sofisticada ou leve",
        "tool_proficiencies": "Ferramentas de ladrão",
        "armor_training": "Armaduras leves",
        "starting_equipment": "Armadura de couro, 2 adagas, espada curta, arco curto, aljava com 20 flechas, ferramentas de ladrão, pacote de ladino e 8 PO ou 100 PO"
    },
    {
        "name": "Bardo",
        "icon": "fas fa-harp",
        "description": "Cantor",
        "primary_ability": "Carisma",
        "hit_point_die": "d8",
        "saving_throw_proficiencies": "Destreza, Carisma",
        "skill_proficiencies": "Escolha quaisquer 3 perícias",
        "weapon_proficiencies": "Armas simples",
        "tool_proficiencies": "Escolha 3 instrumentos musicais",
        "armor_training": "Armaduras leves",
        "starting_equipment": "Armadura de couro, 2 cdagas, instrumento musical de sua escolha, kit do artista e 19 PO; ou 90 PO"
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
        "starting_equipment": "Camisão de malha, escudo, maça, símbolo sagrado, pacote de sacerdote e 7 PO; ou 110 PO"
    },
    {
        "name": "Druida",
        "icon": "fas fa-bear-paw",
        "description": "",
        "primary_ability": "Sabedoria",
        "hit_point_die": "d8",
        "saving_throw_proficiencies": "Inteligência, Sabedoria",
        "skill_proficiencies": "Escolha duas entre: Arcanismo, Lidar com Animais, Intuição, Medicina, Natureza, Persuasão, Religião, Sobrevivência",
        "weapon_proficiencies": "Armas simples",
        "tool_proficiencies": "Kit de herbalismo",
        "armor_training": "Armaduras leves, escudos",
        "starting_equipment": "Armadura de couro, escudo, foice, foco druídico(cajado), pacote de explorador, kit de herbalismo e 9 PO; ou 50 PO"
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
        "starting_equipment": "Camisão de malha, espada grande, mangual, 8 javelins, pacote de masmorra / Armadura de couro batido, cimitarra, espda curta, arco longo, aljava com 20 flechas, pacote de masmorra e 11 PO; ou 155 PO"
    },
    {
        "name": "Monge",
        "icon": "fas fa-fist",
        "description": "",
        "primary_ability": "Destreza ou Sabedoria",
        "hit_point_die": "d8",
        "saving_throw_proficiencies": "Força, Constituição",
        "skill_proficiencies": "Escolha duas entre: Acrobacia, Atletismo, História, Intuição, Religião, Furtividade",
        "weapon_proficiencies": "Armas simples, armas marciais com propriedade leve",
        "tool_proficiencies": "Escolha uma entre: Ferramenta de artesão ou instrumento musical",
        "armor_training": "Nenhuma",
        "starting_equipment": "Lança, 5 adagas, ferramenta de artesão ou instrumento musical, pacote de explorador e 11 PO; ou 50 PO"
    },
    {
        "name": "Paladino",
        "icon": "fas fa-shield",
        "description": "",
        "primary_ability": "Força e Carisma",
        "hit_point_die": "d10",
        "saving_throw_proficiencies": "Sabedoria, Carisma",
        "skill_proficiencies": "Escolha duas entre: Atletismo, Intuição, Intimidação, Medicina, Persuasão, Religião",
        "weapon_proficiencies": "Armas simples, armas marciais",
        "tool_proficiencies": "Nenhuma",
        "armor_training": "Armaduras leves, armaduras médias, armaduras pesadas, escudos",
        "starting_equipment": "Camisão de malha, escudo, espada grande, 6 javelins, símbolo sagrado, pacote de sacerdote e 9 PO ou 150 PO"
    },
    {
        "name": "Caçador",
        "icon": "fas fa-arrow",
        "description": "",
        "primary_ability": "Destreza e Sabedoria",
        "hit_point_die": "d10",
        "saving_throw_proficiencies": "Força, Destreza",
        "skill_proficiencies": "Escolha três entre: Lidar com Animais, Atletismo, Intuição, Investigação, Natureza, Percepção, Furtividade, Sobrevivência",
        "weapon_proficiencies": "Armas simples, armas marciais",
        "tool_proficiencies": "Nenhuma",
        "armor_training": "Armaduras leves, armaduras médias, escudos",
        "starting_equipment": "Armadura de couro batido, cimitarra, espada curta, arco longo, aljava com 20 flechas, foco druídico(flecha de visco), pacote de explorador e 7 PO ou 150 PO"
    },
    {
        "name": "Feiticeiro",
        "icon": "fas fa-fire",
        "description": "",
        "primary_ability": "Carisma",
        "hit_point_die": "d6",
        "saving_throw_proficiencies": "Constituição, Carisma",
        "skill_proficiencies": "Escolha duas entre: Arcanismo, Enganação, Intuição, Intimidação, Persuasão, Religião",
        "weapon_proficiencies": "Armas simples",
        "tool_proficiencies": "Nenhuma",
        "armor_training": "Nenhuma",
        "starting_equipment": "Lança, 2 adagas, foco arcano(cristal), pacote de masmorra e 28 PO ou 50 PO"
    },
    {
        "name": "Bruxo",
        "icon": "fas fa-eye",
        "description": "",
        "primary_ability": "Carisma",
        "hit_point_die": "d8",
        "saving_throw_proficiencies": "Sabedoria, Carisma",
        "skill_proficiencies": "Escolha duas entre: Arcanismo, Enganação, História, Intimidação, Investigaçãon, Natureza, Religião",
        "weapon_proficiencies": "Armas simples",
        "tool_proficiencies": "Nenhuma",
        "armor_training": "Armaduras leves",
        "starting_equipment": "Armadura de couro, foice, 2 adagas, foco arcano(orbe), livro(ocultismo), pacote de estudioso e 15 PO ou 100 PO"
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
