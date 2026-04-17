"""General equipment data from OSRIC 3.0 Player Guide."""

# (name, weight_lbs, cost_gp)
GENERAL_EQUIPMENT: list[tuple[str, float, float]] = [
    ("Backpack", 0.0, 2.0),
    ("Waterskin", 3.0, 1.0),
    ("Rations, standard x7", 14.0, 14.0),
    ("Torches x6", 6.0, 0.06),
    ("Rope, hemp 50ft", 10.0, 1.0),
    ("Flint and steel", 0.0, 1.0),
]

# Class-specific required equipment
CLASS_REQUIRED_EQUIPMENT: dict[str, list[tuple[str, float, float]]] = {
    "Cleric": [("Holy symbol, pewter", 0.0, 5.0)],
    "Druid": [("Holy symbol, pewter", 0.0, 5.0)],
    "Paladin": [("Holy symbol, pewter", 0.0, 5.0)],
    "Thief": [("Thieves' tools", 1.0, 30.0)],
    "Assassin": [("Thieves' tools", 1.0, 30.0)],
}

# Adventuring gear: purchased in order until budget runs out
ADVENTURING_GEAR: list[tuple[str, float, float]] = [
    ("Backpack", 0.0, 2.0),
    ("Waterskin", 3.0, 1.0),
    ("Rations, standard x7", 14.0, 14.0),
    ("Torches x6", 6.0, 0.06),
    ("Rope, hemp 50ft", 10.0, 1.0),
    ("Flint and steel", 0.0, 1.0),
]
