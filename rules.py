from enum import Enum



class ArmorCategory(Enum):
    NONE = "none"
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"

    

def ability_modifier(score: int) -> int:
    return (score - 10) // 2

def proficiency_bonus(level: int) -> int:
    return 2 + (level - 1) // 4

def skill_bonus(score: int, prof_bonus: int, proficient: bool = False, expertise: bool = False) -> int:
    if expertise:
        return ability_modifier(score) + (2 * prof_bonus)
    if proficient:
        return ability_modifier(score) + prof_bonus
    return ability_modifier(score)
 
def saving_throw_bonus(score: int, prof_bonus: int, proficient: bool = False) -> int:
    if proficient:
        return ability_modifier(score) + prof_bonus
    return ability_modifier(score)

def passive_score(skill_bonus: int) -> int:
    return 10 + skill_bonus

def initiative_bonus(dex_modifier: int, additional_bonus: int = 0) -> int:
    return dex_modifier + additional_bonus

def armor_class(armor_base: int, dex_modifier: int, armor: ArmorCategory, shield: bool = False, additional_bonus: int = 0) -> int:
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
    return 8 + proficiency_bonus + spell_ability_mod

def spell_attack_bonus(proficiency_bonus: int, spell_ability_mod: int) -> int:
    return proficiency_bonus + spell_ability_mod

