from app.services.barbarian.select_choices_skill_proficiencies import BarbarianSelectChoicesSkillProficiencies
from app.services.bard.select_choices_skill_proficiencies import BardSelectChoicesSkillProficiencies

cleric = BardSelectChoicesSkillProficiencies(level=1)

options = cleric.get_level_options()

choices = cleric.get_choices_only()
print(choices)


