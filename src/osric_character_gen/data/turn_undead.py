"""Turn undead table from OSRIC 3.0 Player Guide."""

# Turn undead at level 1: (type, example, roll_needed)
# "—" means cannot turn
TURN_UNDEAD_LEVEL_1: list[tuple[str, str, int | str]] = [
    ("Type 1", "Skeleton", 10),
    ("Type 2", "Zombie", 13),
    ("Type 3", "Ghoul", 16),
    ("Type 4", "Shadow", 19),
    ("Type 5", "Wight", 20),
    ("Type 6", "Ghast", "—"),
]
