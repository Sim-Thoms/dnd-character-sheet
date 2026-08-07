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

def get_ac(character: dict, dex_modifier: int) -> int:
    armor_base = character["combat"]["armor_class"]["armor_base"]
    shield = character["combat"]["armor_class"]["shield"]
    additional_bonus = character["combat"]["armor_class"]["additional_bonus"]

    armor = character["combat"]["armor_class"]["armor_category"]
    if armor == "none":
        armor_category = ArmorCategory.NONE
    elif armor == "light":
        armor_category = ArmorCategory.LIGHT
    elif armor == "medium": 
        armor_category = ArmorCategory.MEDIUM
    elif armor == "heavy":
        armor_category = ArmorCategory.HEAVY

    return armor_class(armor_base, dex_modifier, armor_category, shield, additional_bonus)

def get_initiative_bonus(character: dict, dex_modifier: int) -> int:
    additional_bonus = character["combat"]["initiative"]["additional_bonus"]
    return initiative_bonus(dex_modifier, additional_bonus)

def get_spell_save_dc(proficiency_bonus_value: int, spell_ability_mod: int) -> int:
    return spell_save_dc(spell_ability_mod, proficiency_bonus_value)

def get_spell_attack_bonus(proficiency_bonus_value: int, spell_ability_mod: int) -> int:
    return spell_attack_bonus(spell_ability_mod, proficiency_bonus_value)