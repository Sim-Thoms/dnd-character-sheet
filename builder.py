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



ABILITIES = [
    "strength",
    "dexterity",   
    "constitution",  
    "intelligence",
    "wisdom",        
    "charisma",
]



def get_ability_modifiers(character: dict) -> dict:
    scores = character["ability"]["ability_scores"]
    return {ability: ability_modifier(score) for ability, score in scores.items()}

def get_skill_bonuses(character: dict) -> dict:
    bonus_dict = {}
    skills = character["ability"]["skills"]
    scores = character["ability"]["ability_scores"]
    prof_bonus = proficiency_bonus(character["identity"]["level"]) 
    for skill in SKILL_ABILITIES:
        score = scores.get(SKILL_ABILITIES.get(skill))
        expertise, proficient = False, False
        if skills.get(skill) == "expertise":
            expertise = True
        elif skills.get(skill) == "proficient":
            proficient = True
        bonus = skill_bonus(score, prof_bonus, proficient, expertise)
        bonus_dict[skill] = {
            "bonus": bonus,
            "proficient": proficient,
            "expertise": expertise,
            "passive_score": passive_score(bonus),
        }
    return bonus_dict

def get_saving_throw_bonuses(character: dict) -> dict:
    saving_throw_dict = {}
    scores = character["ability"]["ability_scores"]
    saving_throw_proficiencies = character["ability"]["saving_throw_proficiencies"]
    prof_bonus = proficiency_bonus(character["identity"]["level"])
    for ability, score in scores.items():
        proficient = False
        if ability in saving_throw_proficiencies:
            proficient = True
        saving_throw_dict[ability] = saving_throw_bonus(score, prof_bonus, proficient)
    return saving_throw_dict

def get_armor_class(character: dict, dex_modifier: int) -> int:
    armors = character["equipment_and_currency"]["equipment"]["armor"]
    shield = character["equipment_and_currency"]["equipment"]["shield"]
    additional_bonus = character["combat"]["armor_class"]["additional_bonus"]

    armor_base = 10
    armor_category = ArmorCategory.NONE
    for armor in armors:
        if armor["equipped"] == True:
            armor_base = armor["armor_base"]
            if armor["armor_category"] == "none":
                armor_category = ArmorCategory.NONE
            elif armor["armor_category"] == "light":
                armor_category = ArmorCategory.LIGHT
            elif armor["armor_category"] == "medium":
                armor_category = ArmorCategory.MEDIUM
            elif armor["armor_category"] == "heavy":
                armor_category = ArmorCategory.HEAVY

    return armor_class(armor_base, dex_modifier, armor_category, shield, additional_bonus)

def get_initiative_bonus(character: dict, dex_modifier: int) -> int:
    additional_bonus = character["combat"]["initiative"]["additional_bonus"]
    return initiative_bonus(dex_modifier, additional_bonus)

def get_spell_save_dc(proficiency_bonus_value: int, spell_ability_mod: int) -> int:
    return spell_save_dc(spell_ability_mod, proficiency_bonus_value)

def get_spell_attack_bonus(proficiency_bonus_value: int, spell_ability_mod: int) -> int:
    return spell_attack_bonus(spell_ability_mod, proficiency_bonus_value)

def assemble_character_data(character: dict) -> dict:
    character_data = {}

    # Identity
    character_data["identity"] = character["identity"]

    # Abilities
    character_data["ability"] = {}
    character_data["ability"]["ability_scores"] = character["ability"]["ability_scores"]
    character_data["ability"]["ability_modifiers"] = get_ability_modifiers(character)
    character_data["ability"]["saving_throw"] = get_saving_throw_bonuses(character)
    character_data["ability"]["skills"] = get_skill_bonuses(character)

    # Combat
    character_data["combat"] = {}
    character_data["combat"]["hp"] = {
        "maximum_hp": character["combat"]["hp"]["maximum_hp"],
        "hit_dice": character["combat"]["hp"]["hit_dice"],
    }
    character_data["combat"]["speed"] = character["combat"]["speed"]
    character_data["combat"]["armor_class"] = get_armor_class(
        character, character_data["ability"]["ability_modifiers"]["dexterity"]
    )
    character_data["combat"]["initiative"] = get_initiative_bonus(
        character, character_data["ability"]["ability_modifiers"]["dexterity"]
    )

    # Equipment & Currency
    character_data["equipment_and_currency"] = character["equipment_and_currency"]

    # Features & Traits
    character_data["features_and_traits"] = character["features_and_traits"]

    # Spells
    proficiency_bonus_value = proficiency_bonus(character_data["identity"]["level"])
    spell_ability = character["spell"]["spellcasting_ability"]
    spell_ability_mod = character_data["ability"]["ability_modifiers"][spell_ability]
    character_data["spell"] = {}
    character_data["spell"]["spell_save_dc_value"] = get_spell_save_dc(proficiency_bonus_value, spell_ability_mod)
    character_data["spell"]["spell_attack_bonus_value"] = get_spell_attack_bonus(proficiency_bonus_value, spell_ability_mod)
    character_data["spell"]["spell_slots"] = character["spell"]["spell_slots"]
    character_data["spell"]["spell_list"] = character["spell"]["spell_list"]

    return character_data