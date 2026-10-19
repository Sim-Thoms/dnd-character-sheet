from jinja2 import Environment, FileSystemLoader
from datetime import date
import re
from db import (
    get_character
)
from builder import(
    assemble_character_data,
    SKILL_ABILITIES,
    ABILITY_ABBREVIATIONS,
)


CHARACTER_NAME = "Mossy Endoxy"


## Load character data 
character = get_character(CHARACTER_NAME)
character_data = assemble_character_data(character)



def paragraphs(text):
    """Split a description into paragraphs on blank lines, collapsing wrapped lines."""
    paras = re.split(r"\n\s*\n", str(text or ""))
    return [re.sub(r"\s+", " ", p).strip() for p in paras if p.strip()]


## Render the mobile template
env = Environment(loader=FileSystemLoader("templates"))
env.filters["paragraphs"] = paragraphs
template = env.get_template("mobile.html.jinja2")
html_output = template.render(
    character_data=character_data,
    skill_abilities=SKILL_ABILITIES,
    ability_abbreviations=ABILITY_ABBREVIATIONS,
)


## Write the self-contained HTML file, named after the character and the date it was generated
run_date = date.today().isoformat()
output_path = f"character_sheets/{character.identity.name} ({run_date}).html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"Wrote {output_path}")