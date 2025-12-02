import json
import os
from config import basedir


class ZGeneralSelectChoicesSkillProficiencies:
    def __init__(self, level, json_path=None):
        self.level = level
        if json_path is None:
            self.json_path = os.path.join(basedir, 'app', 'db', 'character_classes', 'zgeneral.json')
        else:
            self.json_path = json_path
        self.data = self._load_json()

    def _load_json(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{self.json_path}' não encontrado.")
            return None
        except json.JSONDecodeError:
            print(f"Erro: Arquivo '{self.json_path}' não é um JSON válido.")
            return None

    def get_level_options(self):
        if not self.data:
            return None

        data = self.data.get('zgeneral', {})
        progression = data.get('progression', {})

        level_key = str(self.level)

        if level_key not in progression:
            return {
                'level': self.level,
                'message': f'Nenhuma opção disponível para o nível {self.level}',
                'options': []
            }

        level_options = progression[level_key]

        return {
            'level': self.level,
            'class_name': data.get('name', 'ZGeneral'),
            'options': level_options
        }

    def get_choices_only(self):
        level_data = self.get_level_options()

        if not level_data or not level_data.get('options'):
            return []

        choices = [
            option for option in level_data['options']
            if option.get('type') == 'choice'
        ]

        return choices

    def get_features_only(self):
        level_data = self.get_level_options

    def print_level_options(self):
        pass