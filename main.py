import yaml
import pprint
from rules import(
    proficiency_bonus
)
from builder import(
    get_ability_modifiers,
    get_skill_bonuses, 
    get_saving_throw_bonuses,
    get_ac,
    get_initiative_bonus,
    get_spell_save_dc,
    get_spell_attack_bonus
)



# yaml file to load 
YAML_FILE = "Mossy Endoxy.yaml"



with open(f"data/{YAML_FILE}") as character_sheet:
    cs = yaml.safe_load(character_sheet)

modifiers_dict = get_ability_modifiers(cs)
skill_bonus_dict = get_skill_bonuses(cs)
saving_throw_dict = get_saving_throw_bonuses(cs)


dex_modifier = modifiers_dict["dexterity"]
armor_class_value = get_ac(cs, dex_modifier)
initiative_bonus_value = get_initiative_bonus(cs, dex_modifier)

level = cs["identity"]["level"]
proficiency_bonus_value = proficiency_bonus(level)
spell_ability = cs["spells"]["spellcasting_ability"]
spell_ability_mod = modifiers_dict[spell_ability]
spell_save_dc_value = get_spell_save_dc(proficiency_bonus_value, spell_ability_mod)
spell_attack_bonus_value = get_spell_attack_bonus(proficiency_bonus_value, spell_ability_mod)






print(spell_save_dc_value, spell_attack_bonus_value)