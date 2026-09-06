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

ABILITY_ABBREVIATIONS = {
    "strength": "Str",
    "dexterity": "Dex",
    "constitution": "Con",
    "intelligence": "Int",
    "wisdom": "Wis",
    "charisma": "Cha",
}

DEFAULT_ACCENT_COLOR = "#5f5f5f"  # fallback for any class not listed below
CLASS_ACCENT_COLORS = {
    "ranger": "#2f6d4f",
}



def get_ability_modifiers(character: dict) -> dict:
    """
    Retrieve the ability modifiers for each ability of the character.

    param:: character: A dictionary containing the character's data.
    return:: A dictionary containing the ability modifiers for each ability, calculated based on the character's ability scores.
    """
    scores = character["ability"]["ability_scores"]
    return {ability: ability_modifier(score) for ability, score in scores.items()}

def get_skill_bonuses(character: dict) -> dict:
    """
    Retrieve the skill bonuses for each skill of the character.
    
    param:: character: A dictionary containing the character's data.
    return:: A dictionary containing the skill bonuses for each skill, calculated based on the character's ability scores, proficiency bonus, and skill proficiencies.
    """
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
    """
    Retrieve the saving throw bonuses for each ability of the character.

    param:: character: A dictionary containing the character's data.
    return:: A dictionary containing the saving throw bonuses for each ability, calculated based on the character's ability scores, proficiency bonus, and saving throw proficiencies.
    """
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
    """
    Retrieve the armor class for the character.

    param:: character: A dictionary containing the character's data.
    param:: dex_modifier: The ability modifier for the character's dexterity score.
    return:: The armor class for the character, calculated based on their armor and dexterity modifier.
    """
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
    """
    Retrieve the initiative bonus for the character.

    param:: character: A dictionary containing the character's data.
    param:: dex_modifier: The ability modifier for the character's dexterity score.
    return:: The initiative bonus for the character, calculated based on their dexterity modifier and any additional bonuses specified in their combat data.
    """
    additional_bonus = character["combat"]["initiative"]["additional_bonus"]
    return initiative_bonus(dex_modifier, additional_bonus)

def get_spell_save_dc(proficiency_bonus_value: int, spell_ability_mod: int) -> int:
    """
    Retrieve the spell save DC for the character.
    
    param:: proficiency_bonus_value: The proficiency bonus value for the character.
    param:: spell_ability_mod: The ability modifier for the spellcasting ability.
    return:: The spell save DC for the character.
    """
    return spell_save_dc(spell_ability_mod, proficiency_bonus_value)

def get_spell_attack_bonus(proficiency_bonus_value: int, spell_ability_mod: int) -> int:
    """
    Retrieve the spell attack bonus for the character.

    param:: proficiency_bonus_value: The proficiency bonus value for the character.
    param:: spell_ability_mod: The ability modifier for the spellcasting ability.
    return:: The spell attack bonus for the character.
    """
    return spell_attack_bonus(spell_ability_mod, proficiency_bonus_value)

def get_accent_color(character: dict) -> str:
    """
    Get the accent color for the character based on their class.
    
    param:: character: A dictionary containing the character's data.
    return:: A string representing the accent color for the character's class. If the class is not found in the predefined colors, a default color is returned.
    """
    class_name = character["identity"]["class"].lower()
    return CLASS_ACCENT_COLORS.get(class_name, DEFAULT_ACCENT_COLOR)

def get_weapon_attacks(character: dict) -> list:
    """
    Retrieve the attacks for each weapon the character is wielding.

    param:: character: A dictionary containing the character's data.
    return:: A list of dictionaries, each containing the attack information for a weapon, including name, to-hit bonus, damage dice, damage bonus, damage type, and range.
    """
    prof_bonus = proficiency_bonus(character["identity"]["level"])
    scores = character["ability"]["ability_scores"]
    attacks = []
    for weapon in character["equipment_and_currency"]["equipment"]["weapons"]:
        if not weapon.get("equipped"):
            continue
        ability = weapon.get("ability_used")
        ability_mod = ability_modifier(scores[ability]) if ability in scores else 0
        to_hit = ability_mod + weapon.get("attack_roll_bonus", 0)
        if weapon.get("proficient"):
            to_hit += prof_bonus
        attacks.append({
            "name": weapon["name"],
            "to_hit": to_hit,
            "damage_dice": weapon["damage_dice"],
            "damage_bonus": ability_mod + weapon.get("damage_bonus", 0),
            "damage_type": weapon["damage_type"],
            "range": weapon.get("range"),
        })
    return attacks

def get_maximum_hp(character: dict) -> int:
    """
    Retrieve the maximum hit points for the character.

    param:: character: A dictionary containing the character's data.
    return:: The maximum hit points for the character, calculated based on their level, hit dice, and constitution modifier.
    """
    level = character["identity"]["level"]
    level_hp = character["combat"]["hp"]["level_hp"]
    total_level_hp = 0
    for hp in level_hp:
        total_level_hp += hp
    return total_level_hp + (level * ability_modifier(character["ability"]["ability_scores"]["constitution"]))

def assemble_character_data(character: dict) -> dict:
    """
    Assemble character data into a structured dictionary for rendering in templates.
    
    param:: character: A dictionary containing the character's data.
    return:: A structured dictionary containing the character's data, including identity, abilities, combat stats, equipment, features, and spells. 
    """
    character_data = {}

    # Identity
    character_data["identity"] = character["identity"]
    character_data["identity"]["accent_color"] = get_accent_color(character)

    proficiency_bonus_value = proficiency_bonus(character_data["identity"]["level"])
    character_data["identity"]["proficiency_bonus"] = proficiency_bonus_value
    

    # Abilities
    character_data["ability"] = {}
    character_data["ability"]["ability_scores"] = character["ability"]["ability_scores"]
    character_data["ability"]["ability_modifiers"] = get_ability_modifiers(character)
    character_data["ability"]["saving_throw"] = get_saving_throw_bonuses(character)
    character_data["ability"]["skills"] = get_skill_bonuses(character)

    # Combat
    character_data["combat"] = {}
    character_data["combat"]["hp"] = {
        "maximum_hp": get_maximum_hp(character),
        "hit_dice": character["combat"]["hp"]["hit_dice"],
    }
    character_data["combat"]["speed"] = character["combat"]["speed"]
    character_data["combat"]["armor_class"] = get_armor_class(
        character, character_data["ability"]["ability_modifiers"]["dexterity"]
    )
    character_data["combat"]["initiative"] = get_initiative_bonus(
        character, character_data["ability"]["ability_modifiers"]["dexterity"]
    )
    character_data["combat"]["attacks"] = get_weapon_attacks(character)

    # Equipment & Currency
    character_data["equipment_and_currency"] = character["equipment_and_currency"]

    # Features & Traits
    character_data["features_and_traits"] = character["features_and_traits"]

    # Spells
    spell_ability = character["spell"]["spellcasting_ability"]
    spell_ability_mod = character_data["ability"]["ability_modifiers"][spell_ability]
    character_data["spell"] = {}
    character_data["spell"]["spellcasting_ability"] = spell_ability
    character_data["spell"]["spell_save_dc_value"] = get_spell_save_dc(proficiency_bonus_value, spell_ability_mod)
    character_data["spell"]["spell_attack_bonus_value"] = get_spell_attack_bonus(proficiency_bonus_value, spell_ability_mod)
    character_data["spell"]["spell_slots"] = character["spell"]["spell_slots"]
    character_data["spell"]["spell_list"] = character["spell"]["spell_list"]

    return character_data