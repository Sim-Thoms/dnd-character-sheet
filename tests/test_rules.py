from rules import ability_modifier
from rules import proficiency_bonus



def test_ability_modifier():
    assert ability_modifier(12) == 1

def test_proficiency_bonus():
    assert proficiency_bonus(3) == 2



