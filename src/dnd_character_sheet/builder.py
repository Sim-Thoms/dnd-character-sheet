from typing import TypedDict, Any
from dnd_character_sheet.enums import Ability, ArmorCategory, Proficiency, Skill
from dnd_character_sheet.schematic import AbilityScores, Character, Range
from dnd_character_sheet.rules import (
    ability_modifier,
    proficiency_bonus,
    skill_bonus,
    saving_throw_bonus,
    passive_score,
    initiative_bonus,
    armor_class,
    spell_save_dc,
    spell_attack_bonus,
)


SKILL_ABILITIES = {
    Skill.ACROBATICS: Ability.DEXTERITY,
    Skill.ANIMAL_HANDLING: Ability.WISDOM,
    Skill.ARCANA: Ability.INTELLIGENCE,
    Skill.ATHLETICS: Ability.STRENGTH,
    Skill.DECEPTION: Ability.CHARISMA,
    Skill.HISTORY: Ability.INTELLIGENCE,
    Skill.INSIGHT: Ability.WISDOM,
    Skill.INTIMIDATION: Ability.CHARISMA,
    Skill.INVESTIGATION: Ability.INTELLIGENCE,
    Skill.MEDICINE: Ability.WISDOM,
    Skill.NATURE: Ability.INTELLIGENCE,
    Skill.PERCEPTION: Ability.WISDOM,
    Skill.PERFORMANCE: Ability.CHARISMA,
    Skill.PERSUASION: Ability.CHARISMA,
    Skill.RELIGION: Ability.INTELLIGENCE,
    Skill.SLEIGHT_OF_HAND: Ability.DEXTERITY,
    Skill.STEALTH: Ability.DEXTERITY,
    Skill.SURVIVAL: Ability.WISDOM,
}


ABILITY_ABBREVIATIONS = {
    Ability.STRENGTH: "Str",
    Ability.DEXTERITY: "Dex",
    Ability.CONSTITUTION: "Con",
    Ability.INTELLIGENCE: "Int",
    Ability.WISDOM: "Wis",
    Ability.CHARISMA: "Cha",
}


DEFAULT_ACCENT_COLOR = "#5f5f5f"  # fallback for any class not listed below
CLASS_ACCENT_COLORS = {
    "ranger": "#2f6d4f",
}


class WeaponAttack(TypedDict):
    name: str
    to_hit: int
    damage_dice: str
    damage_bonus: int
    damage_type: str
    range: Range | None

    
def get_ability_modifiers(scores: AbilityScores) -> dict[str, int]:
    """
    Retrieve the ability modifiers for each ability of the character.

    param:: scores: The character's six ability scores.
    return:: A dictionary mapping each ability name to its modifier.
    """
    return {
        ability.value: ability_modifier(getattr(scores, ability.value))
        for ability in Ability
    }


def get_skill_bonuses(character: Character) -> dict[str, dict[str, int | bool]]:
    """
    Retrieve the skill bonuses for each skill of the character.

    param:: character: The validated character.
    return:: A dictionary mapping each skill name to its bonus, proficiency
             state and passive score.
    """
    scores = character.abilities_and_skills.ability_scores
    proficiencies = character.abilities_and_skills.skill_proficiencies
    prof_bonus = proficiency_bonus(character.identity.level)

    bonuses: dict[str, dict[str, int | bool]] = {}
    for skill, ability in SKILL_ABILITIES.items():
        score = getattr(scores, ability.value)
        level = proficiencies.get(skill)
        proficient = level == Proficiency.PROFICIENT
        expertise = level == Proficiency.EXPERTISE

        bonus = skill_bonus(score, prof_bonus, proficient, expertise)
        bonuses[skill.value] = {
            "bonus": bonus,
            "proficient": proficient,
            "expertise": expertise,
            "passive_score": passive_score(bonus),
        }
    return bonuses


def get_saving_throw_bonuses(character: Character) -> dict[str, int]:
    """
    Retrieve the saving throw bonuses for each ability of the character.

    param:: character: The validated character.
    return:: A dictionary mapping each ability name to its saving throw bonus.
    """
    scores = character.abilities_and_skills.ability_scores
    proficiencies = character.abilities_and_skills.saving_throw_proficiencies
    prof_bonus = proficiency_bonus(character.identity.level)

    return {
        ability.value: saving_throw_bonus(
            getattr(scores, ability.value),
            prof_bonus,
            ability in proficiencies,
        )
        for ability in Ability
    }


def get_armor_class(character: Character, dex_modifier: int) -> int:
    """
    Retrieve the armor class for the character.

    param:: character: The validated character.
    param:: dex_modifier: The character's dexterity modifier.
    return:: The armor class, based on equipped armor, shield and dexterity.
    """
    equipment = character.equipment_and_currency

    # The schema guarantees at most one equipped armor.
    equipped = next((armor for armor in equipment.armor if armor.equipped), None)
    armor_base = equipped.armor_base_value if equipped else 10
    armor_category = equipped.armor_category if equipped else ArmorCategory.NONE

    return armor_class(
        armor_base,
        dex_modifier,
        armor_category,
        equipment.shield,
        character.combat.armor_class_bonus,
    )


def get_initiative_bonus(character: Character, dex_modifier: int) -> int:
    """
    Retrieve the initiative bonus for the character.

    param:: character: The validated character.
    param:: dex_modifier: The character's dexterity modifier.
    return:: The initiative bonus.
    """
    return initiative_bonus(dex_modifier, character.combat.initiative_bonus)


def get_spell_save_dc(proficiency_bonus_value: int, spell_ability_mod: int) -> int:
    """
    Retrieve the spell save DC for the character.

    param:: proficiency_bonus_value: The character's proficiency bonus.
    param:: spell_ability_mod: The spellcasting ability modifier.
    return:: The spell save DC.
    """
    return spell_save_dc(spell_ability_mod, proficiency_bonus_value)


def get_spell_attack_bonus(proficiency_bonus_value: int, spell_ability_mod: int) -> int:
    """
    Retrieve the spell attack bonus for the character.

    param:: proficiency_bonus_value: The character's proficiency bonus.
    param:: spell_ability_mod: The spellcasting ability modifier.
    return:: The spell attack bonus.
    """
    return spell_attack_bonus(spell_ability_mod, proficiency_bonus_value)


def get_accent_color(character: Character) -> str:
    """
    Get the accent color for the character based on their class.

    param:: character: The validated character.
    return:: The accent color for the class, or a default if unlisted.
    """
    return CLASS_ACCENT_COLORS.get(character.identity.class_.lower(), DEFAULT_ACCENT_COLOR)


def get_weapon_attacks(character: Character) -> list[WeaponAttack]:
    """
    Retrieve the attacks for each weapon the character has equipped.

    param:: character: The validated character.
    return:: A list of attack dictionaries, one per equipped weapon.
    """
    scores = character.abilities_and_skills.ability_scores
    prof_bonus = proficiency_bonus(character.identity.level)

    attacks: list[WeaponAttack] = []
    for weapon in character.equipment_and_currency.weapons:
        if not weapon.equipped:
            continue

        ability_mod = ability_modifier(getattr(scores, weapon.ability_used.value))
        to_hit = ability_mod + weapon.attack_roll_bonus
        if weapon.proficient:
            to_hit += prof_bonus

        attacks.append({
            "name": weapon.name,
            "to_hit": to_hit,
            "damage_dice": weapon.damage_dice,
            "damage_bonus": ability_mod + weapon.damage_bonus,
            "damage_type": weapon.damage_type,
            "range": weapon.range,
        })
    return attacks


def get_maximum_hp(character: Character) -> int:
    """
    Retrieve the maximum hit points for the character.

    param:: character: The validated character.
    return:: Maximum HP, from the per-level rolls plus the constitution
             modifier applied at every level.
    """
    con_modifier = ability_modifier(
        character.abilities_and_skills.ability_scores.constitution
    )
    return sum(character.combat.hp.level_hp) + (character.identity.level * con_modifier)


def assemble_character_data(character: Character) -> dict[str, Any]:
    """
    Assemble character data into a structured dictionary for rendering.

    param:: character: The validated character.
    return:: A dictionary of raw and computed values for the template.
    """
    character_data: dict[str, Any] = {}

    # Identity — model_dump(by_alias=True) keeps the key as `class`, not `class_`.
    identity = character.identity.model_dump(by_alias=True)
    proficiency_bonus_value = proficiency_bonus(character.identity.level)
    identity["accent_color"] = get_accent_color(character)
    identity["proficiency_bonus"] = proficiency_bonus_value
    character_data["identity"] = identity

    # Abilities
    ability_modifiers = get_ability_modifiers(character.abilities_and_skills.ability_scores)
    character_data["ability"] = {
        "ability_scores": character.abilities_and_skills.ability_scores.model_dump(),
        "ability_modifiers": ability_modifiers,
        "saving_throw": get_saving_throw_bonuses(character),
        "skills": get_skill_bonuses(character),
    }

    # Combat
    dex_modifier = ability_modifiers[Ability.DEXTERITY.value]
    character_data["combat"] = {
        "hp": {
            "maximum_hp": get_maximum_hp(character),
            "hit_dice": character.combat.hp.hit_dice.value,
        },
        "speed": character.combat.speed,
        "armor_class": get_armor_class(character, dex_modifier),
        "initiative": get_initiative_bonus(character, dex_modifier),
        "attacks": get_weapon_attacks(character),
    }

    # Equipment & Currency
    character_data["equipment_and_currency"] = character.equipment_and_currency.model_dump(mode="json")

    # Features & Traits
    character_data["features_and_traits"] = [
        feature.model_dump(mode="json") for feature in character.features_and_traits
    ]

    # Spells — absent entirely for non-casters.
    if character.spellcasting is None:
        character_data["spell"] = None
    else:
        spellcasting = character.spellcasting
        spell_ability_mod = ability_modifiers[spellcasting.spellcasting_ability.value]
        character_data["spell"] = {
            "spellcasting_ability": spellcasting.spellcasting_ability.value,
            "spell_save_dc_value": get_spell_save_dc(
                proficiency_bonus_value, spell_ability_mod
            ),
            "spell_attack_bonus_value": get_spell_attack_bonus(
                proficiency_bonus_value, spell_ability_mod
            ),
            "spell_slots": spellcasting.spell_slots,
            "spell_list": [spell.model_dump(mode="json") for spell in spellcasting.spell_list],
        }

    return character_data