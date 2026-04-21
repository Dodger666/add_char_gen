"""Saving throw tables from OSRIC 3.0 Player Guide."""

from osric_character_gen.models.character import ClassName

# Level 1 saving throws (kept for backward compat references)
SAVING_THROWS_LEVEL_1: dict[ClassName, tuple[int, int, int, int, int]] = {
    ClassName.ASSASSIN: (14, 16, 13, 12, 15),
    ClassName.CLERIC: (14, 16, 10, 13, 15),
    ClassName.DRUID: (14, 16, 10, 13, 15),
    ClassName.FIGHTER: (16, 17, 14, 15, 17),
    ClassName.ILLUSIONIST: (11, 15, 14, 13, 12),
    ClassName.MAGIC_USER: (11, 15, 14, 13, 12),
    ClassName.MONK: (14, 16, 13, 12, 15),
    ClassName.PALADIN: (14, 15, 12, 13, 15),
    ClassName.RANGER: (16, 17, 14, 15, 17),
    ClassName.THIEF: (14, 16, 13, 12, 15),
}

# Full progression: class group → list of (max_level, aimed, breath, death, petri, spells)
# Entries checked top-down; first entry where level <= max_level is used.
_FIGHTER_SAVES: list[tuple[int, int, int, int, int, int]] = [
    (2, 16, 17, 14, 15, 17),
    (4, 15, 16, 13, 14, 16),
    (6, 13, 13, 11, 12, 14),
    (8, 12, 12, 10, 11, 13),
    (10, 10, 9, 8, 9, 11),
    (12, 9, 8, 7, 8, 10),
    (14, 7, 5, 5, 6, 8),
    (16, 6, 4, 4, 5, 7),
    (18, 5, 4, 3, 4, 6),
    (20, 4, 3, 2, 3, 5),
]

_PALADIN_SAVES: list[tuple[int, int, int, int, int, int]] = [
    (2, 14, 15, 12, 13, 15),
    (4, 13, 14, 11, 12, 14),
    (6, 11, 11, 9, 10, 12),
    (8, 10, 10, 8, 9, 11),
    (10, 8, 7, 6, 7, 9),
    (12, 7, 6, 5, 6, 8),
    (14, 5, 3, 3, 4, 6),
    (16, 4, 2, 2, 3, 5),
    (18, 3, 2, 1, 2, 4),
    (20, 2, 1, 1, 1, 3),
]

_CLERIC_SAVES: list[tuple[int, int, int, int, int, int]] = [
    (3, 14, 16, 10, 13, 15),
    (6, 13, 15, 9, 12, 14),
    (9, 11, 13, 7, 10, 12),
    (12, 10, 12, 6, 9, 11),
    (15, 8, 10, 4, 7, 9),
    (18, 7, 9, 3, 6, 8),
    (20, 5, 7, 2, 5, 6),
]

_THIEF_SAVES: list[tuple[int, int, int, int, int, int]] = [
    (4, 14, 16, 13, 12, 15),
    (8, 12, 15, 12, 11, 13),
    (12, 10, 13, 11, 10, 11),
    (16, 8, 11, 9, 8, 9),
    (20, 6, 9, 7, 6, 7),
]

_MAGIC_USER_SAVES: list[tuple[int, int, int, int, int, int]] = [
    (5, 11, 15, 14, 13, 12),
    (10, 9, 13, 13, 11, 10),
    (15, 7, 11, 11, 9, 8),
    (20, 5, 9, 10, 7, 6),
]

# Map each class to its save progression table
SAVING_THROW_TABLES: dict[ClassName, list[tuple[int, int, int, int, int, int]]] = {
    ClassName.FIGHTER: _FIGHTER_SAVES,
    ClassName.PALADIN: _PALADIN_SAVES,
    ClassName.RANGER: _FIGHTER_SAVES,
    ClassName.CLERIC: _CLERIC_SAVES,
    ClassName.DRUID: _CLERIC_SAVES,
    ClassName.THIEF: _THIEF_SAVES,
    ClassName.ASSASSIN: _THIEF_SAVES,
    ClassName.MONK: _THIEF_SAVES,
    ClassName.MAGIC_USER: _MAGIC_USER_SAVES,
    ClassName.ILLUSIONIST: _MAGIC_USER_SAVES,
}


def get_saving_throws(class_name: ClassName, level: int) -> tuple[int, int, int, int, int]:
    """Return (aimed, breath, death, petri, spells) for given class and level."""
    table = SAVING_THROW_TABLES[class_name]
    for max_lvl, aimed, breath, death, petri, spells in table:
        if level <= max_lvl:
            return aimed, breath, death, petri, spells
    # If level exceeds table, use last entry
    return table[-1][1], table[-1][2], table[-1][3], table[-1][4], table[-1][5]
