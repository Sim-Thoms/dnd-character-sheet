import yaml
import pprint
from builder import(
    get_ability_modifiers,
    get_skill_bonuses, 
    get_saving_throw_bonuses,
    get_ac,
    get_initiative_bonus
)



# yaml file to load 
YAML_FILE = "Mossy Endoxy.yaml"



with open(f"data/{YAML_FILE}") as character_sheet:
    cs = yaml.safe_load(character_sheet)

modifiers_dict = get_ability_modifiers(cs)
skill_bonus_dict = get_skill_bonuses(cs)
saving_throw_dict = get_saving_throw_bonuses(cs)


dex_modifier = modifiers_dict["dexterity"]
armor_class = get_ac(cs, dex_modifier)
initiative_bonus = get_initiative_bonus(cs, dex_modifier)


print(armor_class, initiative_bonus)