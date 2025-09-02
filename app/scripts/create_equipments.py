from app import create_app, db
from app.models import Mastery, Property, Weapon

app = create_app()

MASTERIES_DATA = [
    {
        "slug": "cleave", "name": "Abrir Caminho",
        "description": "Se você atingir uma criatura com uma jogada de ataque corpo a corpo usando esta arma, você pode fazer uma jogada de ataque corpo a corpo com a arma contra uma segunda criatura a até 5ft da primeira que também esteja ao seu alcance. Em caso de acerto, a segunda criatura sofre o dano da arma, mas não adicione seu modificador de habilidade a esse dano, a menos que o modificador seja negativo. Você pode fazer este ataque extra apenas uma vez por turno."
    },
    {
        "slug": "graze", "name": "Arranhar",
        "description": "Se sua jogada de ataque com esta arma errar uma criatura, você pode causar dano a essa criatura igual ao modificador de habilidade que você usou para fazer a jogada de ataque. Este dano é do mesmo tipo causado pela arma, e o dano só pode ser aumentado melhorando o modificador de habilidade."
    },
    {
        "slug": "nick", "name": "Incisão",
        "description": "Ao realizar o ataque extra da propriedade Leve, você pode fazê-lo como parte da ação de ataque em vez de uma Ação Bônus. Você pode realizar este ataque extra apenas uma vez por turno."
    },
    {
        "slug": "push", "name": "Empurrar",
        "description": "Se você atingir uma criatura com esta arma, você pode empurrá-la até 10ft para longe de você, se ela for Grande ou menor."
    },
    {
        "slug": "sap", "name": "Fluido Vital",
        "description": "Se você atingir uma criatura com esta arma, ela terá Desvantagem em sua próxima jogada de ataque antes do início do seu próximo turno."
    },
    {
        "slug": "slow", "name": "Lentidão",
        "description": "Se você atingir uma criatura com esta arma e causar dano a ela, você pode reduzir sua Velocidade em 10ft até o início do seu próximo turno. Se a criatura for atingida mais de uma vez por armas que tenham esta propriedade, a redução de velocidade não excede 10ft."
    },
    {
        "slug": "topple", "name": "Derrubar",
        "description": "Se você atingir uma criatura com esta arma, você pode forçá-la a realizar um teste de resistência de Constituição (CD 8 mais o modificador de habilidade usado para realizar a jogada de ataque e seu Bônus de Proficiência). Em caso de falha, a criatura fica propensa à condição de Caída."
    },
    {
        "slug": "vex", "name": "Irritante",
        "description": "Se você atingir uma criatura com esta arma e causar dano a ela, você terá Vantagem na sua próxima jogada de ataque contra aquela criatura antes do final do seu próximo turno."
    }
]

PROPERTIES_DATA = [
    {
        "slug": "ammunition", "name": "Munição",
        "description": "Você pode usar uma arma com a propriedade Munição para realizar um ataque à distância somente se tiver munição para disparar. O tipo de munição necessária é especificado com o alcance da arma. Cada ataque gasta uma peça de munição. Sacar a munição faz parte do ataque (você precisa de uma mão livre para carregar uma arma de uma mão). Após um combate, você pode gastar 1 minuto para recuperar metade da munição (arredondada para baixo) usada no combate, o restante é perdido."
    },
    {
        "slug": "finesse", "name": "Acuidade",
        "description": "Ao realizar um ataque com uma arma de Acuidade, use o modificador de Força ou Destreza de sua escolha para as jogadas de ataque e dano. Você deve usar o mesmo modificador para ambas as jogadas."
    },
    {
        "slug": "heavy", "name": "Pesado",
        "description": "Você tem desvantagem em jogadas de ataque com uma arma Pesada se for uma arma corpo a corpo e seu valor de Força não for pelo menos 13 ou se for uma arma de longo alcance e seu valor de Destreza não for pelo menos 13."
    },
    {
        "slug": "light", "name": "Leve",
        "description": "Ao realizar uma ação de ataque no seu turno e atacar com uma arma Leve, você pode realizar um ataque extra como Ação Bônus posteriormente no mesmo turno. Esse ataque extra deve ser realizado com uma arma Leve diferente, e você não adiciona seu modificador de habilidade ao dano do ataque extra, a menos que esse modificador seja negativo."
    },
    {
        "slug": "loading", "name": "Carregamento",
        "description": "Você pode disparar apenas uma munição de uma arma de Carregamento quando usa uma ação, uma Ação Bônus ou uma Reação para dispará-la, independentemente do número de ataques que você normalmente pode fazer."
    },
    {
        "slug": "range", "name": "Alcance",
        "description": "Uma arma de Alcance tem o alcance entre parênteses após a propriedade Munição ou Arremesso. O alcance lista dois números. O primeiro é o alcance normal da arma em pés, e o segundo é o alcance longo da arma. Ao atacar um alvo além do alcance normal, você tem Desvantagem na jogada de ataque. Você não pode atacar um alvo além do alcance longo."
    },
    {
        "slug": "reach", "name": "Abrangente",
        "description": "Uma arma Abrangente adiciona 5ft ao seu alcance quando você ataca com ela, bem como ao determinar seu alcance para Ataques de Oportunidade com ela."
    },
    {
        "slug": "thrown", "name": "Arremesso",
        "description": "Se uma arma tiver a propriedade Arremesso, você pode arremessá-la para realizar um ataque à distância e sacá-la como parte do ataque. Se a arma for uma arma corpo a corpo, use o mesmo modificador de habilidade para as jogadas de ataque e dano que você usa para um ataque corpo a corpo com essa arma."
    },
    {
        "slug": "two_handed", "name": "Duas Mãos",
        "description": "Uma arma de Duas Mãos requer as duas mãos quando você ataca com ela."
    },
    {
        "slug": "versatile", "name": "Versátil",
        "description": "Uma arma versátil pode ser usada com uma ou duas mãos. Um valor de dano entre parênteses aparece junto com a propriedade. A arma causa o maior dano quando usada com as duas mãos para realizar um ataque corpo a corpo."
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