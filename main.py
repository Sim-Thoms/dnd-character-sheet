import yaml
import pprint
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
from builder import(
    get_ability_modifiers,
    get_skill_bonuses, 
    get_saving_throw_bonuses
)



# yaml file to load 
YAML_FILE = "Mossy Endoxy.yaml"



with open(f"data/{YAML_FILE}") as character_sheet:
    cs = yaml.safe_load(character_sheet)

modifiers_dict = get_ability_modifiers(cs)
skill_bonus_dict = get_skill_bonuses(cs)
saving_throw_dict = get_saving_throw_bonuses(cs)






pprint.pprint(get_saving_throw_bonuses(cs))