from pydantic import BaseModel, Field, model_validator
from typing import Annotated
from enums import(
    Ability,
    Skill,
    Proficiency,
    Dice,
    Label,
    Component,
    ArmorCategory,
)



# ======================= Shared Aliases =======================
NonEmptyStr = Annotated[str, Field(min_length=1)]
NonNegativeInt = Annotated[int, Field(ge=0)]

# ========================== Identity ==========================
class Identity(BaseModel):
    name: NonEmptyStr
    race: NonEmptyStr
    level: int = Field(ge=1, le=20)
    class_: NonEmptyStr = Field(alias='class')
    subclass: NonEmptyStr | None = None

# ===================== Abilities & Skills =====================
ScoreValue = Annotated[int, Field(ge=1, le=30)]

class AbilityScores(BaseModel):
    strength: ScoreValue
    dexterity: ScoreValue
    constitution: ScoreValue
    intelligence: ScoreValue
    wisdom: ScoreValue
    charisma: ScoreValue

class AbilitiesAndSkills(BaseModel):
    ability_scores: AbilityScores
    saving_throw_proficiencies: list[Ability] = Field(min_length=2, max_length=2)
    skill_proficiencies: dict[Skill, Proficiency] = {}

# =========================== Combat ===========================
class HP(BaseModel):
    hit_dice: Dice
    level_hp: list[Annotated[int, Field(ge=1)]] = Field(min_length=1)

class Combat(BaseModel):
    armor_class_bonus: int = 0
    initiative_bonus: int = 0
    speed: int 
    hp: HP

# ===================== Features & Traits ======================
class FeatureOrTrait(BaseModel):
    name: NonEmptyStr
    label: Label
    description: NonEmptyStr  

# ======================== Spellcasting ========================
class Spell(BaseModel):
    name: NonEmptyStr
    level: Annotated[int, Field(ge=0, le=9)]
    casting_time: NonEmptyStr
    spell_range: NonEmptyStr
    duration: NonEmptyStr
    components: list[Component] = Field(min_length=1)
    materials: NonEmptyStr | None = None
    prepared: bool = False
    description: NonEmptyStr


class Spellcasting(BaseModel):
    spellcasting_ability: Ability
    spell_slots: dict[  # key: spell level, value: number of slots
        Annotated[int, Field(ge=1, le=9)], 
        Annotated[int, Field(ge=1)]
    ] = {}
    spell_list: list[Spell] = []

# =================== Equipment and Currency ===================
class Range(BaseModel):
    normal_range: NonNegativeInt 
    long_range: NonNegativeInt 

class Weapon(BaseModel):
    name: NonEmptyStr
    damage_dice: NonEmptyStr
    damage_type: NonEmptyStr
    ability_used: Ability
    equipped: bool = False
    range: Range | None = None
    quantity: NonNegativeInt = 1
    proficient: bool = False
    damage_bonus: int = 0
    attack_roll_bonus: int = 0

class Armor(BaseModel):
    name: NonEmptyStr
    armor_base_value: NonNegativeInt
    armor_category: ArmorCategory
    equipped: bool = False
    proficient: bool = False
    stealth_penalty: bool = False
    strength_requirement: NonNegativeInt = 0

class Item(BaseModel):
    name: NonEmptyStr
    description: NonEmptyStr
    quantity: NonNegativeInt = 1

class Currency(BaseModel):
    copper: NonNegativeInt = 0 # 10cp = 1sp
    silver: NonNegativeInt = 0 # 5sp = 1ep
    electrum: NonNegativeInt = 0 # 2ep = 1gp
    gold: NonNegativeInt = 0 # 10gp = 1pp
    platinum: NonNegativeInt = 0

class EquipmentAndCurrency(BaseModel):
    currency: Currency
    weapons: list[Weapon] = []
    armor: list[Armor] = []
    items: list[Item] = []
    shield: bool = False

    @model_validator(mode="after")
    def single_equipped_armor(self):
        equipped_armor = [armor.name for armor in self.armor if armor.equipped]
        if len(equipped_armor) > 1:
            names = ", ".join(equipped_armor)
            raise ValueError(f"At most one armor can be equipped; equipped: {names}")
        return self    

# ========================== Character =========================
class Character(BaseModel):
    identity: Identity
    abilities_and_skills: AbilitiesAndSkills
    combat: Combat
    equipment_and_currency: EquipmentAndCurrency
    features_and_traits: list[FeatureOrTrait] = []
    spellcasting: Spellcasting | None = None

    @model_validator(mode="after")
    def level_hp_matches_level(self):
        level_hp_count = len(self.combat.hp.level_hp)
        if level_hp_count != self.identity.level:
            raise ValueError(
                f"level_hp must contain one value per character level; "
                f"level is {self.identity.level}, but level_hp contains {level_hp_count} values"
            )
        return self