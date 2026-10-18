import pytest
from pydantic import ValidationError
from schematic import AbilityScores, Character


# ============================ Fixtures ============================
# Fixtures re-run for every test, so each test gets its own fresh dict.
# That means a test can mutate what it receives without affecting others.


@pytest.fixture
def ability_scores():
    return {
        "strength": 10,
        "dexterity": 16,
        "constitution": 14,
        "intelligence": 10,
        "wisdom": 15,
        "charisma": 8,
    }


@pytest.fixture
def character_data(ability_scores):
    return {
        "identity": {
            "name": "Mossy Endoxy",
            "race": "Mothkin",
            "level": 4,
            "class": "Ranger",
            "subclass": "Swarmkeeper",
        },
        "abilities_and_skills": {
            "ability_scores": ability_scores,
            "saving_throw_proficiencies": ["strength", "dexterity"],
            "skill_proficiencies": {
                "stealth": "proficient",
                "perception": "expertise",
            },
        },
        "combat": {
            "speed": 30,
            "hp": {"hit_dice": "d10", "level_hp": [10, 6, 7, 6]},
        },
        "equipment_and_currency": {
            "currency": {"gold": 25},
            "weapons": [
                {
                    "name": "Longbow",
                    "damage_dice": "1d8",
                    "damage_type": "Piercing",
                    "ability_used": "dexterity",
                    "equipped": True,
                    "proficient": True,
                    "range": {"normal_range": 150, "long_range": 600},
                }
            ],
            "armor": [
                {
                    "name": "Leather Armor",
                    "armor_base_value": 11,
                    "armor_category": "light",
                    "equipped": True,
                    "proficient": True,
                }
            ],
        },
        "features_and_traits": [
            {
                "name": "Archery",
                "label": "feature",
                "description": "+2 to attack rolls with ranged weapons.",
            }
        ],
        "spellcasting": {
            "spellcasting_ability": "wisdom",
            "spell_slots": {1: 3},
            "spell_list": [
                {
                    "name": "Hunter's Mark",
                    "level": 1,
                    "casting_time": "1 bonus action",
                    "spell_range": "90 feet",
                    "duration": "Concentration, up to 1 hour",
                    "components": ["verbal"],
                    "prepared": True,
                    "description": "Extra 1d6 damage on hits against the target.",
                }
            ],
        },
    }


# ========================= Baseline sanity ========================


def test_valid_character_loads(character_data):
    character = Character(**character_data)
    assert character.identity.name == "Mossy Endoxy"


# ========================= Ability scores =========================


@pytest.mark.parametrize("score", [1, 30])
def test_ability_score_accepts_boundaries(ability_scores, score):
    ability_scores["strength"] = score
    AbilityScores(**ability_scores)


@pytest.mark.parametrize("score", [0, 31])
def test_ability_score_rejects_out_of_range(ability_scores, score):
    ability_scores["strength"] = score
    with pytest.raises(ValidationError):
        AbilityScores(**ability_scores)


@pytest.mark.parametrize(
    "field",
    ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"],
)
def test_every_ability_score_is_constrained(ability_scores, field):
    """Catches a field that lost its ScoreValue annotation."""
    ability_scores[field] = 31
    with pytest.raises(ValidationError):
        AbilityScores(**ability_scores)


# ============================= Enums ==============================


def test_unknown_skill_is_rejected(character_data):
    character_data["abilities_and_skills"]["skill_proficiencies"]["stelth"] = "proficient"
    with pytest.raises(ValidationError):
        Character(**character_data)


def test_unknown_hit_dice_is_rejected(character_data):
    character_data["combat"]["hp"]["hit_dice"] = "d13"
    with pytest.raises(ValidationError):
        Character(**character_data)


# =========================== Constraints ==========================


@pytest.mark.parametrize(
    "saves",
    [[], ["strength"], ["strength", "dexterity", "wisdom"]],
)
def test_saving_throws_must_be_exactly_two(character_data, saves):
    character_data["abilities_and_skills"]["saving_throw_proficiencies"] = saves
    with pytest.raises(ValidationError):
        Character(**character_data)


def test_empty_name_is_rejected(character_data):
    character_data["identity"]["name"] = ""
    with pytest.raises(ValidationError):
        Character(**character_data)


@pytest.mark.parametrize("level", [-1, 10])
def test_spell_level_out_of_range_is_rejected(character_data, level):
    character_data["spellcasting"]["spell_list"][0]["level"] = level
    with pytest.raises(ValidationError):
        Character(**character_data)


# ======================== Cross-field rules =======================


def test_level_hp_must_match_level(character_data):
    character_data["combat"]["hp"]["level_hp"] = [10, 6, 7]
    with pytest.raises(ValidationError, match="level_hp"):
        Character(**character_data)


def test_at_most_one_armor_equipped(character_data):
    character_data["equipment_and_currency"]["armor"].append(
        {
            "name": "Chain Mail",
            "armor_base_value": 16,
            "armor_category": "heavy",
            "equipped": True,
        }
    )
    with pytest.raises(ValidationError, match="At most one armor"):
        Character(**character_data)


# ============================ Defaults ============================


def test_skill_proficiencies_default_to_empty(character_data):
    del character_data["abilities_and_skills"]["skill_proficiencies"]
    character = Character(**character_data)
    assert character.abilities_and_skills.skill_proficiencies == {}


def test_non_caster_has_no_spellcasting(character_data):
    del character_data["spellcasting"]
    character = Character(**character_data)
    assert character.spellcasting is None


# =========================== Round-trip ===========================


def test_class_round_trips_under_its_yaml_key(character_data):
    """by_alias=True is what keeps the stored key as `class`, not `class_`."""
    dumped = Character(**character_data).model_dump(by_alias=True)
    assert "class" in dumped["identity"]
    assert "class_" not in dumped["identity"]