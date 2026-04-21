"""Turn undead table from OSRIC 3.0 Player Guide."""

# Turn undead at level 1 (kept for backward compat)
TURN_UNDEAD_LEVEL_1: list[tuple[str, str, int | str]] = [
    ("Type 1", "Skeleton", 10),
    ("Type 2", "Zombie", 13),
    ("Type 3", "Ghoul", 16),
    ("Type 4", "Shadow", 19),
    ("Type 5", "Wight", 20),
    ("Type 6", "Ghast", "—"),
]

# Full turn undead table: all undead types across levels
# Each entry: (type, example, {level: roll_needed})
# "T" = automatic turn, "D" = automatic destroy, "—" = cannot turn
_UNDEAD_TYPES: list[tuple[str, str]] = [
    ("Type 1", "Skeleton"),
    ("Type 2", "Zombie"),
    ("Type 3", "Ghoul"),
    ("Type 4", "Shadow"),
    ("Type 5", "Wight"),
    ("Type 6", "Ghast"),
    ("Type 7", "Wraith"),
    ("Type 8", "Mummy"),
    ("Type 9", "Spectre"),
    ("Type 10", "Vampire"),
    ("Type 11", "Ghost"),
    ("Type 12", "Lich"),
    ("Type 13", "Fiend"),
]

# level → list of roll_needed values for each undead type (indices 0-12)
TURN_UNDEAD_TABLE: dict[int, list[int | str]] = {
    1: [10, 13, 16, 19, 20, "—", "—", "—", "—", "—", "—", "—", "—"],
    2: [7, 10, 13, 16, 19, 20, "—", "—", "—", "—", "—", "—", "—"],
    3: [4, 7, 10, 13, 16, 19, 20, "—", "—", "—", "—", "—", "—"],
    4: ["T", "T", 4, 7, 10, 13, 16, 19, 20, "—", "—", "—", "—"],
    5: ["T", "T", "T", 4, 7, 10, 13, 16, 19, 20, "—", "—", "—"],
    6: ["D", "D", "T", "T", 4, 7, 10, 13, 16, 19, 20, "—", "—"],
    7: ["D", "D", "D", "T", "T", 4, 7, 10, 13, 16, 19, 20, "—"],
    8: ["D", "D", "D", "D", "T", "T", 4, 7, 10, 13, 16, 19, 20],
    9: ["D", "D", "D", "D", "D", "T", "T", 4, 7, 10, 13, 16, 19],
}


def get_turn_undead(level: int) -> list[tuple[str, str, int | str]]:
    """Return turn undead table for a cleric at the given level."""
    # Levels 9+ use the level 9 table
    effective = min(level, 9)
    rolls = TURN_UNDEAD_TABLE[effective]
    result = []
    for i, (utype, example) in enumerate(_UNDEAD_TYPES):
        roll = rolls[i]
        # Skip entries that are "—" (cannot turn) and beyond
        if roll == "—":
            continue
        result.append((utype, example, roll))
    return result
