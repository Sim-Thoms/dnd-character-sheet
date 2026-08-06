from rules import(
    ability_modifier, 
    proficiency_bonus, 
    skill_bonus, 
    saving_throw_bonus, 
    passive_score,
    initiative_bonus,
    armor_class,
    spell_save_dc,
    spell_attack_bonus,
    ArmorCategory,
)



SKILL_ABILITIES = {
    "acrobatics": "dexterity",
    "animal handling": "wisdom",
    "arcana": "intelligence",
    "athletics": "strength",
    "deception": "charisma",
    "history": "intelligence",
    "insight": "wisdom",
    "intimidation": "charisma",
    "investigation": "intelligence",
    "medicine": "wisdom",
    "nature": "intelligence",
    "perception": "wisdom", 
    "performance": "charisma",
    "persuasion": "charisma",
    "religion": "intelligence",
    "sleight of hand": "dexterity",   
    "stealth": "dexterity",
    "survival": "wisdom"
}



def get_ability_modifiers(character: dict) -> dict:
    scores = character["abilities"]["ability_scores"]
    return {ability: ability_modifier(score) for ability, score in scores.items()}

def get_skill_bonuses(character: dict) -> dict:
    bonus_dict = {}
    skills = character["abilities"]["skills"]
    scores = character["abilities"]["ability_scores"]
    prof_bonus = proficiency_bonus(character["identity"]["level"]) 
    for skill in SKILL_ABILITIES:
        score = scores.get(SKILL_ABILITIES.get(skill))
        expertise, proficient = False, False
        if skills.get(skill) == "expertise":
            expertise = True
        elif skills.get(skill) == "proficient":
            proficient = True
        bonus_dict[skill] = skill_bonus(score, prof_bonus, proficient, expertise)
    return 

def get_saving_throw_bonuses(character: dict) -> dict:
    saving_throw_dict = {}
    scores = character["abilities"]["ability_scores"]
    saving_throw_proficiencies = character["abilities"]["saving_throw_proficiencies"]
    prof_bonus = proficiency_bonus(character["identity"]["level"])
    for ability, score in scores.items():
        proficient = False
        if ability in saving_throw_proficiencies:
            proficient = True
        saving_throw_dict[ability] = saving_throw_bonus(score, prof_bonus, proficient)
    return saving_throw_dict


