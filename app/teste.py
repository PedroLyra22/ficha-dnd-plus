from app.services.cleric.select_choices_skill_proficiencies import ClericSelectChoicesSkillProficiencies

cleric = ClericSelectChoicesSkillProficiencies(level=3)

options = cleric.get_level_options()

choices = cleric.get_choices_only()
print(choices)

print(cleric.get_features_only())

