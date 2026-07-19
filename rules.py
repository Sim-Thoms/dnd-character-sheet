def ability_modifier(score: int) -> int:
    return (score - 10) // 2

def proficiency_bonus(level: int) -> int:
    return 2 + (level - 1) // 4

def skill_bonus(score: int, prof_bonus: int, proficient: bool = False, expertise: bool = False):
    if proficient == False and expertise == False:
        skill_bonus = ability_modifier(score)
    elif proficient == True and expertise == False: 
        skill_bonus = ability_modifier(score) + prof_bonus
    else:
        skill_bonus = ability_modifier(score) + (2 * prof_bonus)
    return skill_bonus

