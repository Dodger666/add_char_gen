"""Monk-specific progression tables from OSRIC 3.0 Player Guide."""

# Monk AC by level (descending, ascending)
MONK_AC: dict[int, tuple[int, int]] = {
    1: (10, 10),
    2: (9, 11),
    3: (8, 12),
    4: (7, 13),
    5: (6, 14),
    6: (5, 15),
    7: (4, 16),
    8: (3, 17),
    9: (2, 18),
    10: (1, 19),
    11: (0, 20),
    12: (-1, 21),
    13: (-2, 22),
    14: (-3, 23),
    15: (-4, 24),
    16: (-5, 25),
    17: (-6, 26),
}

# Monk weaponless damage by level
MONK_DAMAGE: dict[int, str] = {
    1: "1d3",
    2: "1d3",
    3: "1d3",
    4: "1d4",
    5: "1d4",
    6: "1d6",
    7: "1d6",
    8: "2d4",
    9: "2d4+1",
    10: "2d4+1",
    11: "3d4",
    12: "3d4",
    13: "3d4",
    14: "4d4",
    15: "4d4",
    16: "5d4",
    17: "5d4",
}

# Monk movement by level (feet per round)
MONK_MOVEMENT: dict[int, int] = {
    1: 150,
    2: 150,
    3: 160,
    4: 160,
    5: 170,
    6: 180,
    7: 190,
    8: 200,
    9: 210,
    10: 220,
    11: 230,
    12: 240,
    13: 250,
    14: 260,
    15: 270,
    16: 280,
    17: 290,
}

# Monk special abilities gained by level (cumulative)
MONK_ABILITIES: dict[int, str] = {
    2: "Deflect Missiles (save vs. petrification to negate 1 ranged attack/round)",
    3: "Speak with Animals (at will)",
    4: "Slow Fall (20 ft) — no damage",
    5: "Slow Fall (30 ft), Immune to disease",
    6: "Slow Fall (any distance), Feign Death",
    7: "Self-heal 1d4+level HP once/day",
    8: "Speak with Plants (at will)",
    9: "+1 to saves vs. mental attacks",
    10: "Immune to haste, slow, charm, geas, quest",
    11: "Immune to poison",
    12: "Immune to psionics",
    13: "Quivering Palm (1/week, save vs. death or die)",
}
