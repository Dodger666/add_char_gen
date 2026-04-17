"""Ancestry definitions from OSRIC 3.0 Player Guide."""

from osric_character_gen.models.character import AncestryName, ClassName

# Ability score ranges AFTER adjustments: {ability: (min, max)}
ANCESTRY_SCORE_RANGES: dict[AncestryName, dict[str, tuple[int, int]]] = {
    AncestryName.DWARF: {
        "strength": (8, 18),
        "dexterity": (3, 17),
        "constitution": (12, 19),
        "intelligence": (3, 18),
        "wisdom": (3, 18),
        "charisma": (3, 16),
    },
    AncestryName.ELF: {
        "strength": (3, 18),
        "dexterity": (7, 19),
        "constitution": (6, 18),
        "intelligence": (8, 18),
        "wisdom": (3, 18),
        "charisma": (8, 18),
    },
    AncestryName.GNOME: {
        "strength": (6, 18),
        "dexterity": (3, 18),
        "constitution": (8, 18),
        "intelligence": (7, 18),
        "wisdom": (3, 18),
        "charisma": (3, 18),
    },
    AncestryName.HALF_ELF: {
        "strength": (3, 18),
        "dexterity": (6, 18),
        "constitution": (6, 18),
        "intelligence": (4, 18),
        "wisdom": (3, 18),
        "charisma": (3, 18),
    },
    AncestryName.HALF_ORC: {
        "strength": (6, 18),
        "dexterity": (3, 17),
        "constitution": (13, 19),
        "intelligence": (3, 17),
        "wisdom": (3, 14),
        "charisma": (3, 12),
    },
    AncestryName.HALFLING: {
        "strength": (6, 17),
        "dexterity": (8, 18),
        "constitution": (10, 19),
        "intelligence": (6, 18),
        "wisdom": (3, 17),
        "charisma": (3, 18),
    },
    AncestryName.HUMAN: {
        "strength": (3, 18),
        "dexterity": (3, 18),
        "constitution": (3, 18),
        "intelligence": (3, 18),
        "wisdom": (3, 18),
        "charisma": (3, 18),
    },
}

# Ability score adjustments
ANCESTRY_ADJUSTMENTS: dict[AncestryName, dict[str, int]] = {
    AncestryName.DWARF: {"constitution": 1, "charisma": -1},
    AncestryName.ELF: {"dexterity": 1, "constitution": -1},
    AncestryName.GNOME: {},
    AncestryName.HALF_ELF: {},
    AncestryName.HALF_ORC: {"strength": 1, "constitution": 1, "charisma": -2},
    AncestryName.HALFLING: {"strength": -1, "dexterity": 1},
    AncestryName.HUMAN: {},
}

# Available single classes per ancestry
ANCESTRY_CLASSES: dict[AncestryName, list[ClassName]] = {
    AncestryName.DWARF: [
        ClassName.ASSASSIN,
        ClassName.CLERIC,
        ClassName.FIGHTER,
        ClassName.THIEF,
    ],
    AncestryName.ELF: [
        ClassName.ASSASSIN,
        ClassName.CLERIC,
        ClassName.FIGHTER,
        ClassName.MAGIC_USER,
        ClassName.THIEF,
    ],
    AncestryName.GNOME: [
        ClassName.ASSASSIN,
        ClassName.CLERIC,
        ClassName.FIGHTER,
        ClassName.ILLUSIONIST,
        ClassName.THIEF,
    ],
    AncestryName.HALF_ELF: [
        ClassName.ASSASSIN,
        ClassName.CLERIC,
        ClassName.DRUID,
        ClassName.FIGHTER,
        ClassName.MAGIC_USER,
        ClassName.RANGER,
        ClassName.THIEF,
    ],
    AncestryName.HALF_ORC: [
        ClassName.ASSASSIN,
        ClassName.CLERIC,
        ClassName.FIGHTER,
        ClassName.THIEF,
    ],
    AncestryName.HALFLING: [
        ClassName.FIGHTER,
        ClassName.DRUID,
        ClassName.THIEF,
    ],
    AncestryName.HUMAN: list(ClassName),
}

# Physical characteristics formulas
# (base_inches, num_dice, die_sides) for height
ANCESTRY_HEIGHT: dict[AncestryName, tuple[int, int, int]] = {
    AncestryName.DWARF: (48, 3, 4),
    AncestryName.ELF: (54, 3, 4),
    AncestryName.GNOME: (34, 3, 4),
    AncestryName.HALF_ELF: (60, 4, 4),
    AncestryName.HALF_ORC: (66, 3, 4),
    AncestryName.HALFLING: (34, 3, 4),
    AncestryName.HUMAN: (64, 3, 4),
}

# (base_lbs, num_dice, die_sides) for weight
ANCESTRY_WEIGHT: dict[AncestryName, tuple[int, int, int]] = {
    AncestryName.DWARF: (150, 5, 10),
    AncestryName.ELF: (70, 5, 10),
    AncestryName.GNOME: (45, 4, 10),
    AncestryName.HALF_ELF: (90, 5, 10),
    AncestryName.HALF_ORC: (150, 5, 10),
    AncestryName.HALFLING: (45, 4, 10),
    AncestryName.HUMAN: (140, 6, 10),
}

# Starting age: {ancestry: {class: (base, num_dice, die_sides)}}
ANCESTRY_STARTING_AGE: dict[AncestryName, dict[ClassName, tuple[int, int, int]]] = {
    AncestryName.DWARF: {
        ClassName.CLERIC: (250, 2, 20),
        ClassName.FIGHTER: (40, 5, 4),
        ClassName.THIEF: (75, 3, 6),
        ClassName.ASSASSIN: (75, 3, 6),
    },
    AncestryName.ELF: {
        ClassName.CLERIC: (500, 10, 10),
        ClassName.FIGHTER: (130, 5, 6),
        ClassName.MAGIC_USER: (150, 5, 6),
        ClassName.THIEF: (100, 5, 6),
        ClassName.ASSASSIN: (100, 5, 6),
    },
    AncestryName.GNOME: {
        ClassName.CLERIC: (300, 3, 12),
        ClassName.FIGHTER: (60, 5, 4),
        ClassName.ILLUSIONIST: (100, 2, 12),
        ClassName.THIEF: (80, 5, 4),
        ClassName.ASSASSIN: (80, 5, 4),
    },
    AncestryName.HALF_ELF: {
        ClassName.CLERIC: (40, 2, 4),
        ClassName.DRUID: (40, 2, 4),
        ClassName.FIGHTER: (22, 3, 4),
        ClassName.RANGER: (22, 3, 4),
        ClassName.MAGIC_USER: (30, 2, 8),
        ClassName.THIEF: (22, 3, 8),
        ClassName.ASSASSIN: (22, 3, 8),
    },
    AncestryName.HALF_ORC: {
        ClassName.CLERIC: (20, 1, 4),
        ClassName.FIGHTER: (13, 1, 4),
        ClassName.THIEF: (20, 2, 4),
        ClassName.ASSASSIN: (20, 2, 4),
    },
    AncestryName.HALFLING: {
        ClassName.FIGHTER: (20, 3, 4),
        ClassName.DRUID: (40, 3, 4),
        ClassName.THIEF: (40, 2, 4),
    },
    AncestryName.HUMAN: {
        ClassName.CLERIC: (20, 1, 4),
        ClassName.DRUID: (20, 1, 4),
        ClassName.MONK: (20, 1, 4),
        ClassName.FIGHTER: (15, 1, 4),
        ClassName.PALADIN: (15, 1, 4),
        ClassName.RANGER: (15, 1, 4),
        ClassName.MAGIC_USER: (24, 2, 8),
        ClassName.ILLUSIONIST: (24, 2, 8),
        ClassName.THIEF: (20, 1, 4),
        ClassName.ASSASSIN: (20, 1, 4),
    },
}

# Age category thresholds: (youth_max, adult, grizzled, elder, ancient)
ANCESTRY_AGE_CATEGORIES: dict[AncestryName, tuple[int, int, int, int, int]] = {
    AncestryName.DWARF: (50, 51, 150, 250, 350),
    AncestryName.ELF: (174, 175, 550, 875, 1200),
    AncestryName.GNOME: (89, 90, 300, 450, 600),
    AncestryName.HALF_ELF: (39, 40, 100, 175, 250),
    AncestryName.HALF_ORC: (15, 16, 30, 45, 60),
    AncestryName.HALFLING: (32, 33, 68, 101, 144),
    AncestryName.HUMAN: (19, 20, 40, 60, 90),
}

# Age category adjustments: {category: {ability: adjustment}}
AGE_CATEGORY_ADJUSTMENTS: dict[str, dict[str, int]] = {
    "Youth": {"constitution": 1, "wisdom": -1},
    "Adult": {"strength": 1, "wisdom": 1},
    "Grizzled": {"strength": -1, "constitution": -1, "intelligence": 1, "wisdom": 1},
    "Elder": {"strength": -2, "dexterity": -2, "constitution": -1, "wisdom": 1},
    "Ancient": {"strength": -1, "dexterity": -1, "constitution": -1, "intelligence": 1, "wisdom": 1},
}

# Movement rates: base movement in feet
ANCESTRY_MOVEMENT: dict[AncestryName, int] = {
    AncestryName.DWARF: 90,
    AncestryName.ELF: 120,
    AncestryName.GNOME: 90,
    AncestryName.HALF_ELF: 120,
    AncestryName.HALF_ORC: 120,
    AncestryName.HALFLING: 90,
    AncestryName.HUMAN: 120,
}

# Ancestry features (for character sheet display)
ANCESTRY_FEATURES: dict[AncestryName, list[str]] = {
    AncestryName.DWARF: [
        "Giant-Slayers: Giants attack at -4 to hit",
        "Grudge-Bearers: +1 to hit goblins, half-orcs, hobgoblins, orcs",
        "Stalwart: CON-based save bonus vs poison/spells/magic",
        "Stone-Kenning: Detect slopes 75%, new construction 75%, sliding walls 65%, traps 50%, depth 50%",
        "Infravision 60ft",
    ],
    AncestryName.ELF: [
        "Fey Deftness: +1 to hit with bows and short/long swords",
        "Keen Detection: 1/6 passive concealed/secret; 2/6 active secret, 3/6 active concealed",
        "Lightfooted: 4-in-6 surprise (light armor, 90ft from non-lightfooted)",
        "Strength of Will: 90% resist sleep/charm",
        "Cannot be raised/resurrected",
        "Infravision 60ft",
    ],
    AncestryName.GNOME: [
        "Ancestral Foes: +1 to hit kobolds and goblins",
        "Giant-Slayers: Giants attack at -4 to hit",
        "Stalwart: CON-based save bonus vs poison/spells/magic",
        "Stone-Kenning: Slopes 80%, unsafe areas 70%, depth 60%, direction 50%",
        "Infravision 60ft",
    ],
    AncestryName.HALF_ELF: [
        "Keen Detection: Active only: 2/6 secret, 3/6 concealed",
        "Strength of Mind: 30% resist sleep/charm",
        "Infravision 60ft",
    ],
    AncestryName.HALF_ORC: [
        "Infravision 60ft",
        "Cannot be raised/resurrected",
    ],
    AncestryName.HALFLING: [
        "Halfling Marksmanship: +3 to hit with bows/slings",
        "Lightfooted: 4-in-6 surprise (same conditions as elf)",
        "Stalwart: CON-based save bonus vs poison/spells/magic",
        "Infravision 60ft",
    ],
    AncestryName.HUMAN: [
        "Unlimited level advancement",
        "Eligible for dual-classing",
    ],
}

# Stalwart save bonus by CON score (Dwarf, Gnome, Halfling)
STALWART_BONUS: dict[int, int] = {
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 2,
    8: 2,
    9: 2,
    10: 2,
    11: 3,
    12: 3,
    13: 3,
    14: 4,
    15: 4,
    16: 4,
    17: 4,
    18: 5,
    19: 5,
}

STALWART_ANCESTRIES = {AncestryName.DWARF, AncestryName.GNOME, AncestryName.HALFLING}

# Ancestry preference order for each class (used by ancestry selector)
ANCESTRY_PREFERENCE: dict[ClassName, list[AncestryName]] = {
    ClassName.THIEF: [
        AncestryName.HALFLING,
        AncestryName.ELF,
        AncestryName.HALF_ELF,
        AncestryName.HUMAN,
    ],
    ClassName.FIGHTER: [AncestryName.DWARF, AncestryName.HUMAN],
    ClassName.CLERIC: [AncestryName.DWARF, AncestryName.HUMAN],
    ClassName.ILLUSIONIST: [AncestryName.GNOME, AncestryName.HUMAN],
    ClassName.ASSASSIN: [AncestryName.HUMAN],
    ClassName.DRUID: [AncestryName.HUMAN],
    ClassName.MAGIC_USER: [AncestryName.HUMAN],
    ClassName.MONK: [AncestryName.HUMAN],
    ClassName.PALADIN: [AncestryName.HUMAN],
    ClassName.RANGER: [AncestryName.HUMAN],
}

# Languages by ancestry
ANCESTRY_LANGUAGES: dict[AncestryName, list[str]] = {
    AncestryName.DWARF: ["Common", "Dwarfish"],
    AncestryName.ELF: ["Common", "Elven"],
    AncestryName.GNOME: ["Common", "Gnomish"],
    AncestryName.HALF_ELF: ["Common", "Elven"],
    AncestryName.HALF_ORC: ["Common", "Orcish"],
    AncestryName.HALFLING: ["Common", "Halfling"],
    AncestryName.HUMAN: ["Common"],
}
