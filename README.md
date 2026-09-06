# D&D Character Sheet Generator

A Python-generated, self-contained mobile character sheet for D&D 5e (2014 rules + homebrew). Character data lives in local YAML files; running the generator loads a character, computes every derived stat, and renders it into a single self-contained HTML file — no server, no app, nothing to install to actually use the sheet. Open it on a phone or laptop (it just works).

## Features
- Five-page mobile layout: Overview, Abilities & Skills, Combat, Spells, Items & Currency
- Live session state — current HP, spell slots, and death saves with +/− controls, resets on reload rather than being stored
- Tap-to-expand descriptions for features, traits, spells, and inventory items
- Per-class accent color, dark theme, Flavia display font (see license note below)
- Every derived value (ability modifiers, proficiency bonus, AC, spell DC, passive scores, weapon attack/damage bonuses, etc.) is computed from a small set of raw inputs — nothing that can be derived is stored twice

## Tech stack
- Python, managed with [uv](https://docs.astral.sh/uv/)
- Jinja2 for HTML templating
- PyYAML for character authoring and storage
- pytest for the rules engine test suite

## Setup
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it.
2. Clone this repo and `cd` into it.
3. Install dependencies:
4. Create a `raw` folder inside `data/` to hold your character files — this isn't created automatically, and its contents are gitignored.
5. Create a `character_sheets` folder in the project root for the generated sheets — this isn't created automatically either.

## Adding or updating a character
Characters are plain YAML files in `data/raw/`.

To create one, copy `data/character.template.yaml` into `data/raw/` and rename it after your character (e.g. `John Doe.yaml`). The template is commented throughout — it documents which fields exist and what each one expects.

To update one, edit the file directly. The guiding rule is that the YAML holds only what you actively choose: ability scores, proficiencies, equipment, spells known. Anything the rules can derive from those — modifiers, AC, save DCs, passive scores — is computed at render time and should never be written into the file.

Re-run the generator afterward to produce an updated sheet.

## Rendering a character sheet
Loads the character from `data/raw/`, computes every derived stat, and writes a self-contained HTML file to `character_sheets/{name} ({date}).html`. Open it directly in a browser — no server needed.

## Project structure
dnd-character-sheet/
├── data/
│ ├── raw/ # character data (YAML, gitignored)
│ └── character.template.yaml # commented schema reference for new characters
├── templates/
│ └── mobile.html.jinja2 # the character sheet template
├── tests/
│ └── test_rules.py
├── character_sheets/ # generated output (create manually, gitignored)
├── rules.py # pure D&D math, no I/O
├── builder.py # bridges raw character data to rules.py
├── main.py # orchestrator: load → compute → render → write
└── pyproject.toml / uv.lock # dependencies, managed by uv

## Font license note
The character sheet embeds the Flavia font, licensed under 1001Fonts' Free For Personal Use terms. Personal, non-commercial use is fine; the font itself shouldn't be redistributed as a standalone download. Keep that in mind if you fork this repo.