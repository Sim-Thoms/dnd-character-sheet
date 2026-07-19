from rules import ability_modifier, proficiency_bonus, skill_bonus



def test_ability_modifier():
    assert ability_modifier(12) == 1

def test_proficiency_bonus():
    assert proficiency_bonus(3) == 2

def test_skill_bonus():
    assert skill_bonus(12, 2) == 1
    assert skill_bonus(12, 2, True) == 3
    assert skill_bonus(12, 2, True, True) == 5

