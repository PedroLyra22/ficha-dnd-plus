from app import create_app, db
from app.models import Mastery, Property, Weapon

app = create_app()

MASTERIES_DATA = [
    {
        "slug": "nick", "name": "Nick",
        "description": "Ao atacar com uma arma Leve, você pode usar uma Ação Bônus para fazer um ataque com outra arma Leve que esteja em sua outra mão."
    },
    {
        "slug": "sap", "name": "Sap",
        "description": "Se você acertar uma criatura com esta arma, ela tem Desvantagem na próxima jogada de ataque que fizer antes do início do seu próximo turno."
    },
    {
        "slug": "vex", "name": "Vex",
        "description": "Se você acertar uma criatura com esta arma, você tem Vantagem nas jogadas de ataque contra ela até o final do seu próximo turno."
    }
]

PROPERTIES_DATA = [
    {
        "slug": "acuidade", "name": "Acuidade",
        "description": "Permite usar seu modificador de Destreza em vez de Força para as jogadas de ataque e dano."
    },
    {
        "slug": "leve", "name": "Leve",
        "description": "Pequena e fácil de manusear, ideal para combate com duas armas."
    },
    {
        "slug": "arremesso", "name": "Arremesso",
        "description": "Pode ser arremessada para fazer um ataque à distância."
    }
]

WEAPONS_DATA = [
    {
        "name": "Adaga", "weapon_type": "Arma Simples Corpo a Corpo", "damage": "1d4", "damage_type": "Perfurante",
        "cost": "2 PO", "weight": "1 lb",
        "mastery_slug": "nick",
        "property_slugs": ["acuidade", "leve", "arremesso"]
    },
    {
        "name": "Clava", "weapon_type": "Arma Simples Corpo a Corpo", "damage": "1d4", "damage_type": "Concussão",
        "cost": "1 PP", "weight": "2 lb",
        "mastery_slug": "sap",
        "property_slugs": ["leve"]
    },
    {
        "name": "Machadinha", "weapon_type": "Arma Simples Corpo a Corpo", "damage": "1d6", "damage_type": "Cortante",
        "cost": "5 PO", "weight": "2 lb",
        "mastery_slug": "vex",
        "property_slugs": ["leve", "arremesso"]
    }
]


def populate_database():
    with app.app_context():
        db.create_all()

        masteries_map = {}
        properties_map = {}

        for data in MASTERIES_DATA:
            existing = Mastery.query.filter_by(slug=data['slug']).first()
            if not existing:
                new_obj = Mastery(**data)
                db.session.add(new_obj)
                masteries_map[data['slug']] = new_obj
                print(f"Adicionando maestria: {data['name']}")
            else:
                masteries_map[data['slug']] = existing
                print(f"Maestria '{data['name']}' já existe. Pulando.")

        for data in PROPERTIES_DATA:
            existing = Property.query.filter_by(slug=data['slug']).first()
            if not existing:
                new_obj = Property(**data)
                db.session.add(new_obj)
                properties_map[data['slug']] = new_obj
                print(f"Adicionando propriedade: {data['name']}")
            else:
                properties_map[data['slug']] = existing
                print(f"Propriedade '{data['name']}' já existe. Pulando.")

        db.session.commit()

        for data in WEAPONS_DATA:
            existing = Weapon.query.filter_by(name=data['name']).first()
            if not existing:
                mastery_slug = data.pop('mastery_slug')
                property_slugs = data.pop('property_slugs')

                new_weapon = Weapon(**data)

                if mastery_slug in masteries_map:
                    new_weapon.mastery = masteries_map[mastery_slug]

                if property_slugs:
                    new_weapon.properties = [properties_map[slug] for slug in property_slugs if slug in properties_map]

                db.session.add(new_weapon)
                print(f"Adicionando arma: {data['name']}")
            else:
                print(f"Arma '{data['name']}' já existe. Pulando.")

        db.session.commit()
        print("População do banco de dados concluída!")


if __name__ == '__main__':
    populate_database()