from enums import ArmorCategory

    

def ability_modifier(score: int) -> int:
    """
    Calculate the ability modifier for a given ability score.

    param:: score: The ability score.
    return:: The ability modifier.
    """
    return (score - 10) // 2

def proficiency_bonus(level: int) -> int:
    """
    Calculate the proficiency bonus for a given level.

    param:: level: The character's level.
    return:: The proficiency bonus.
    """
    return 2 + (level - 1) // 4

def skill_bonus(score: int, prof_bonus: int, proficient: bool = False, expertise: bool = False) -> int:
    """
    Calculate the skill bonus for a given skill.

    param:: score: The ability score for the skill.
    param:: prof_bonus: The proficiency bonus.
    param:: proficient: Whether the character is proficient in the skill.
    param:: expertise: Whether the character has expertise in the skill.
    return:: The skill bonus.
    """
    if expertise:
        return ability_modifier(score) + (2 * prof_bonus)
    if proficient:
        return ability_modifier(score) + prof_bonus
    return ability_modifier(score)
 
def saving_throw_bonus(score: int, prof_bonus: int, proficient: bool = False) -> int:
    """
    Calculate the saving throw bonus for a given ability.

    param:: score: The ability score.
    param:: prof_bonus: The proficiency bonus.
    param:: proficient: Whether the character is proficient in the saving throw.
    return:: The saving throw bonus.
    """
    if proficient:
        return ability_modifier(score) + prof_bonus
    return ability_modifier(score)

def passive_score(skill_bonus: int) -> int:
    """
    Calculate the passive score for a given skill.

    param:: skill_bonus: The skill bonus.
    return:: The passive score.
    """
    return 10 + skill_bonus

def initiative_bonus(dex_modifier: int, additional_bonus: int = 0) -> int:
    """
    Calculate the initiative bonus for the character.

    param:: dex_modifier: The ability modifier for the character's dexterity score.
    param:: additional_bonus: Any additional bonus to initiative.
    return:: The initiative bonus.
    """
    return dex_modifier + additional_bonus

def armor_class(armor_base: int, dex_modifier: int, armor: ArmorCategory, shield: bool = False, additional_bonus: int = 0) -> int:
    """
    Calculate the armor class for the character.

    param:: armor_base: The base armor class.
    param:: dex_modifier: The ability modifier for the character's dexterity score.
    param:: armor: The category of armor the character is wearing.
    param:: shield: Whether the character is using a shield.
    param:: additional_bonus: Any additional bonus to armor class.
    return:: The armor class for the character.
    """
    if shield:
        shield_value = 2
    else:
        shield_value = 0

    if armor == ArmorCategory.NONE:
        return 10 + dex_modifier + shield_value + additional_bonus
    elif armor == ArmorCategory.LIGHT:
        return armor_base + dex_modifier + shield_value + additional_bonus
    elif armor == ArmorCategory.MEDIUM:
        return armor_base + min(dex_modifier, 2) + shield_value + additional_bonus
    elif armor == ArmorCategory.HEAVY: 
        return armor_base + shield_value + additional_bonus

def spell_save_dc(proficiency_bonus: int, spell_ability_mod: int) -> int:
    """
    Calculate the spell save DC for the character.

    param:: proficiency_bonus: The proficiency bonus value for the character.
    param:: spell_ability_mod: The ability modifier for the spellcasting ability.
    return:: The spell save DC for the character.
    """
    return 8 + proficiency_bonus + spell_ability_mod

def spell_attack_bonus(proficiency_bonus: int, spell_ability_mod: int) -> int:
    """
    Calculate the spell attack bonus for the character.

    param:: proficiency_bonus: The proficiency bonus value for the character.
    param:: spell_ability_mod: The ability modifier for the spellcasting ability.
    return:: The spell attack bonus for the character.
    """
    return proficiency_bonus + spell_ability_mod


