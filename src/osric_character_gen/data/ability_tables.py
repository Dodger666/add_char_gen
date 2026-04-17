"""Ability score bonus lookup tables from OSRIC 3.0 Player Guide."""

# STR bonuses: key is STR score (or tuple for exceptional)
# Values: (to_hit, damage, encumbrance_lbs, minor_test, major_test)
# Minor test = chance on d6, Major test = chance on d100
STRENGTH_TABLE: dict[int | str, tuple[int, int, int, str, str]] = {
    3: (-3, -1, 0, "1", "0%"),
    4: (-2, -1, 10, "1", "0%"),
    5: (-2, -1, 10, "1", "0%"),
    6: (-1, 0, 20, "1", "0%"),
    7: (-1, 0, 20, "1", "0%"),
    8: (0, 0, 35, "1-2", "1%"),
    9: (0, 0, 35, "1-2", "1%"),
    10: (0, 0, 35, "1-2", "2%"),
    11: (0, 0, 35, "1-2", "2%"),
    12: (0, 0, 45, "1-2", "4%"),
    13: (0, 0, 45, "1-2", "4%"),
    14: (0, 0, 55, "1-2", "7%"),
    15: (0, 0, 55, "1-2", "7%"),
    16: (0, 1, 70, "1-3", "10%"),
    17: (1, 1, 85, "1-3", "13%"),
    18: (1, 2, 110, "1-3", "16%"),
    # Exceptional strength ranges — keyed by string
    "18.01-50": (1, 3, 135, "1-3", "20%"),
    "18.51-75": (2, 3, 160, "1-4", "25%"),
    "18.76-90": (2, 4, 185, "1-4", "30%"),
    "18.91-99": (2, 5, 235, "1-4*", "35%"),
    "18.00": (3, 6, 300, "1-5**", "40%"),
}


def get_strength_bonuses(strength: int, exceptional: int | None = None) -> tuple[int, int, int, str, str]:
    """Return (to_hit, damage, encumbrance, minor_test, major_test)."""
    if strength == 18 and exceptional is not None:
        if exceptional == 100:
            return STRENGTH_TABLE["18.00"]
        if exceptional <= 50:
            return STRENGTH_TABLE["18.01-50"]
        if exceptional <= 75:
            return STRENGTH_TABLE["18.51-75"]
        if exceptional <= 90:
            return STRENGTH_TABLE["18.76-90"]
        return STRENGTH_TABLE["18.91-99"]
    return STRENGTH_TABLE.get(strength, (0, 0, 35, "—", "—"))


# DEX bonuses: (surprise, missile_to_hit, initiative, ac_adj_desc, ac_adj_asc, agility_save)
DEXTERITY_TABLE: dict[int, tuple[int, int, int, int, int, int]] = {
    3: (-3, -3, 3, 4, -4, -4),
    4: (-2, -2, 2, 3, -3, -3),
    5: (-1, -1, 1, 2, -2, -2),
    6: (0, 0, 0, 1, -1, -1),
    7: (0, 0, 0, 0, 0, 0),
    8: (0, 0, 0, 0, 0, 0),
    9: (0, 0, 0, 0, 0, 0),
    10: (0, 0, 0, 0, 0, 0),
    11: (0, 0, 0, 0, 0, 0),
    12: (0, 0, 0, 0, 0, 0),
    13: (0, 0, 0, 0, 0, 0),
    14: (0, 0, 0, 0, 0, 0),
    15: (0, 0, 0, -1, 1, 1),
    16: (1, 1, -1, -2, 2, 2),
    17: (2, 2, -2, -3, 3, 3),
    18: (3, 3, -3, -4, 4, 4),
    19: (3, 3, -3, -4, 4, 4),
}


def get_dexterity_bonuses(
    dexterity: int,
) -> tuple[int, int, int, int, int, int]:
    """Return (surprise, missile_to_hit, initiative, ac_adj_desc, ac_adj_asc, agility_save)."""
    if dexterity <= 3:
        return DEXTERITY_TABLE[3]
    if dexterity >= 19:
        return DEXTERITY_TABLE[19]
    return DEXTERITY_TABLE.get(dexterity, (0, 0, 0, 0, 0, 0))


# CON bonuses: (hp_mod_non_fighter, hp_mod_fighter, resurrection_pct, system_shock_pct)
CONSTITUTION_TABLE: dict[int, tuple[int, int, int, int]] = {
    3: (-2, -2, 40, 35),
    4: (-1, -1, 45, 40),
    5: (-1, -1, 50, 45),
    6: (-1, -1, 55, 50),
    7: (0, 0, 60, 55),
    8: (0, 0, 65, 60),
    9: (0, 0, 70, 65),
    10: (0, 0, 75, 70),
    11: (0, 0, 80, 75),
    12: (0, 0, 85, 80),
    13: (0, 0, 88, 83),
    14: (0, 0, 92, 88),
    15: (1, 1, 94, 91),
    16: (2, 2, 96, 95),
    17: (2, 3, 98, 97),
    18: (2, 4, 100, 99),
    19: (2, 5, 100, 99),
}

FIGHTER_TYPES = {"Fighter", "Paladin", "Ranger"}


def get_constitution_bonuses(constitution: int, class_name: str) -> tuple[int, int, int]:
    """Return (hp_mod, resurrection_pct, system_shock_pct)."""
    if constitution <= 3:
        row = CONSTITUTION_TABLE[3]
    elif constitution >= 19:
        row = CONSTITUTION_TABLE[19]
    else:
        row = CONSTITUTION_TABLE.get(constitution, (0, 0, 75, 70))
    hp_mod = row[1] if class_name in FIGHTER_TYPES else row[0]
    return hp_mod, row[2], row[3]


# INT: max_additional_languages
INTELLIGENCE_TABLE: dict[int, int] = {
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 1,
    9: 1,
    10: 2,
    11: 2,
    12: 3,
    13: 3,
    14: 4,
    15: 4,
    16: 5,
    17: 6,
    18: 7,
    19: 8,
}


def get_intelligence_bonuses(intelligence: int) -> int:
    """Return max_additional_languages."""
    if intelligence <= 3:
        return 0
    if intelligence >= 19:
        return 8
    return INTELLIGENCE_TABLE.get(intelligence, 0)


# WIS: mental_save_modifier
WISDOM_MENTAL_SAVE: dict[int, int] = {
    3: -3,
    4: -2,
    5: -1,
    6: -1,
    7: -1,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 1,
    16: 2,
    17: 3,
    18: 4,
    19: 5,
}

# WIS bonus spells: list of (min_wis, spell_level, bonus_slots)
WISDOM_BONUS_SPELLS: list[tuple[int, int, int]] = [
    (13, 1, 1),  # WIS 13: +1 first-level
    (14, 1, 1),  # WIS 14: +1 first-level (total +2)
    (15, 2, 1),  # WIS 15: +1 second-level
    (16, 2, 1),  # WIS 16: +1 second-level (total +2)
    (17, 3, 1),  # WIS 17: +1 third-level
    (18, 4, 1),  # WIS 18: +1 fourth-level
]


def get_wisdom_bonuses(wisdom: int) -> tuple[int, list[dict[str, int]]]:
    """Return (mental_save_mod, bonus_spell_list)."""
    if wisdom <= 3:
        mental = WISDOM_MENTAL_SAVE[3]
    elif wisdom >= 19:
        mental = WISDOM_MENTAL_SAVE[19]
    else:
        mental = WISDOM_MENTAL_SAVE.get(wisdom, 0)

    bonus_spells = []
    for min_wis, spell_level, slots in WISDOM_BONUS_SPELLS:
        if wisdom >= min_wis:
            bonus_spells.append({"level": spell_level, "slots": slots})
    return mental, bonus_spells


# CHA: (sidekick_limit, loyalty_mod, reaction_mod)
CHARISMA_TABLE: dict[int, tuple[int, int, int]] = {
    3: (1, -30, -25),
    4: (1, -25, -20),
    5: (2, -20, -15),
    6: (2, -15, -10),
    7: (3, -10, -5),
    8: (3, -5, 0),
    9: (4, 0, 0),
    10: (4, 0, 0),
    11: (4, 0, 0),
    12: (5, 0, 0),
    13: (5, 0, 5),
    14: (6, 5, 10),
    15: (7, 15, 15),
    16: (8, 20, 25),
    17: (10, 30, 30),
    18: (15, 40, 35),
    19: (20, 50, 40),
}


def get_charisma_bonuses(charisma: int) -> tuple[int, int, int]:
    """Return (sidekick_limit, loyalty_mod, reaction_mod)."""
    if charisma <= 3:
        return CHARISMA_TABLE[3]
    if charisma >= 19:
        return CHARISMA_TABLE[19]
    return CHARISMA_TABLE.get(charisma, (4, 0, 0))
