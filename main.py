from jinja2 import Environment, FileSystemLoader
from datetime import date
import yaml
import re
from builder import(
    assemble_character_data,
    SKILL_ABILITIES,
    ABILITY_ABBREVIATIONS,
)



## Load character data 
with open("data/raw/Mossy Endoxy.yaml", "r", encoding="utf-8") as f:
    character_yaml = yaml.safe_load(f)
character_data = assemble_character_data(character_yaml)

## Render the mobile template
env = Environment(loader=FileSystemLoader("templates"))
env.filters["paragraphs"] = lambda text: [p.strip() for p in re.split(r"\n+", text or "") if p.strip()]
template = env.get_template("mobile.html.jinja2")
html_output = template.render(
    character_data=character_data,
    skill_abilities=SKILL_ABILITIES,
    ability_abbreviations=ABILITY_ABBREVIATIONS,
)

## Write the self-contained HTML file, named after the character and the date it was generated
run_date = date.today().isoformat()
output_path = f"character_sheets/{character_data['identity']['name']} ({run_date}).html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"Wrote {output_path}")