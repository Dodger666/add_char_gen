"""Armor data from OSRIC 3.0 Player Guide."""

# (name, ac_desc, ac_asc, weight_lbs, movement_cap, cost_gp)
ARMOR_TABLE: list[tuple[str, int, int, float, int, float]] = [
    ("Leather", 8, 12, 15.0, 120, 5.0),
    ("Padded", 8, 12, 10.0, 90, 4.0),
    ("Studded Leather", 7, 13, 20.0, 90, 15.0),
    ("Ring Mail", 7, 13, 35.0, 90, 30.0),
    ("Scale/Lamellar", 6, 14, 40.0, 60, 45.0),
    ("Chain Mail", 5, 15, 30.0, 90, 75.0),
    ("Splint", 4, 16, 40.0, 60, 80.0),
    ("Banded", 4, 16, 35.0, 90, 90.0),
    ("Plate Mail", 3, 17, 45.0, 60, 400.0),
]

# Shield data: (name, weight, cost_gp)
SHIELD_TABLE: list[tuple[str, float, float]] = [
    ("Small Shield", 5.0, 10.0),
    ("Medium Shield", 8.0, 12.0),
    ("Large Shield", 10.0, 15.0),
]

# Armor purchase priority by class (best to worst, within restrictions)
ARMOR_PRIORITY: dict[str, list[str]] = {
    "heavy": [
        "Chain Mail",
        "Banded",
        "Scale/Lamellar",
        "Ring Mail",
        "Studded Leather",
        "Leather",
    ],
    "light": ["Studded Leather", "Leather"],
    "thief": ["Studded Leather", "Leather", "Padded"],
    "druid": ["Leather"],
    "none": [],
}
