# D&D Character Sheet Generator

A Python-generated, self-contained mobile character sheet for D&D 5e (2014 rules + homebrew). 

## Features
- Five-page mobile layout: Overview, Abilities & Skills, Combat, Spells, Items & Currency
- Live session state — current HP, spell slots, and death saves with +/− controls, resets on reload rather than being stored
- Tap-to-expand descriptions for features, traits, spells, and inventory items
- Per-class accent color, dark theme, Flavia display font (see license note below)
- Every derived value (ability modifiers, proficiency bonus, AC, spell DC, passive scores, weapon attack/damage bonuses, etc.) is computed from a small set of raw inputs — nothing that can be derived is stored twice

## Font license note
The character sheet embeds the Flavia font, licensed under 1001Fonts' Free For Personal Use terms. Personal, non-commercial use is fine; the font itself shouldn't be redistributed as a standalone download. Keep that in mind if you fork this repo.