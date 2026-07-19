from rules import ability_modifier, proficiency_bonus, skill_bonus, saving_throw_bonus, passive_score



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
