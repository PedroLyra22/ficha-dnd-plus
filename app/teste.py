from app.services.barbarian.select_choices_skill_proficiencies import ClericSelectChoicesSkillProficiencies

cleric = BarbarianSelectChoicesSkillProficiencies(level=3)

options = cleric.get_level_options()

choices = cleric.get_choices_only()
print(choices)

print(cleric.get_features_only())

