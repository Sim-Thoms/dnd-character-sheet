from rules import(
    ability_modifier, 
    proficiency_bonus, 
    skill_bonus, 
    saving_throw_bonus, 
    passive_score,
    initiative_bonus,
    armor_class,
    ArmorCategory,
) 



def test_ability_modifier():
    assert ability_modifier(12) == 1

def test_proficiency_bonus():
    assert proficiency_bonus(3) == 2

def test_skill_bonus():
    assert skill_bonus(12, 2) == 1
    assert skill_bonus(12, 2, True) == 3
    assert skill_bonus(12, 2, True, True) == 5

def test_saving_throw_bonus():
    assert saving_throw_bonus(12, 2) == 1
    assert saving_throw_bonus(12, 2, True) == 3

def test_passive_score():
    assert passive_score(2) == 12

def test_initiative_bonus():
    assert initiative_bonus(3) == 3
    assert initiative_bonus(3, 2) == 5

def test_armor_class():
    assert armor_class(0, 2, ArmorCategory.NONE, False, 3) == 15
    assert armor_class(12, 2, ArmorCategory.LIGHT) == 14
    assert armor_class(12, 4, ArmorCategory.MEDIUM, True, 1) == 17
    assert armor_class(12, 1, ArmorCategory.MEDIUM, True, 1) == 16
    assert armor_class(15, 4, ArmorCategory.HEAVY, False, 5) == 20