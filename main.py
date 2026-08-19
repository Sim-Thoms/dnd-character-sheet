import yaml
from builder import(
    assemble_character_data,
)



# yaml file to load 
YAML_FILE = "Mossy Endoxy.yaml"

with open(f"data/{YAML_FILE}") as character_sheet:
    cs = yaml.safe_load(character_sheet)

character_data = assemble_character_data(cs)


print(character_data)