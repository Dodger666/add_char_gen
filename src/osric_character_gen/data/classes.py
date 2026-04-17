"""Class definitions from OSRIC 3.0 Player Guide."""

from osric_character_gen.models.character import Alignment, ClassName

# Minimum ability scores per class
# {ClassName: {ability: min_score}} — None means no minimum
CLASS_MINIMUMS: dict[ClassName, dict[str, int | None]] = {
    ClassName.ASSASSIN: {
        "strength": 12,
        "dexterity": 12,
        "constitution": 6,
        "intelligence": 11,
        "wisdom": 6,
        "charisma": None,
    },
    ClassName.CLERIC: {
        "strength": 6,
        "dexterity": None,
        "constitution": 6,
        "intelligence": 6,
        "wisdom": 9,
        "charisma": 6,
    },
    ClassName.DRUID: {
        "strength": 6,
        "dexterity": None,
        "constitution": 6,
        "intelligence": 6,
        "wisdom": 12,
        "charisma": 15,
    },
    ClassName.FIGHTER: {
        "strength": 9,
        "dexterity": 6,
        "constitution": 7,
        "intelligence": 3,
        "wisdom": 6,
        "charisma": 6,
    },
    ClassName.ILLUSIONIST: {
        "strength": 6,
        "dexterity": 16,
        "constitution": None,
        "intelligence": 15,
        "wisdom": 6,
        "charisma": 6,
    },
    ClassName.MAGIC_USER: {
        "strength": None,
        "dexterity": 6,
        "constitution": 6,
        "intelligence": 9,
        "wisdom": 6,
        "charisma": 6,
    },
    ClassName.MONK: {
        "strength": 10,
        "dexterity": 15,
        "constitution": None,
        "intelligence": None,
        "wisdom": 10,
        "charisma": None,
    },
    ClassName.PALADIN: {
        "strength": 12,
        "dexterity": 6,
        "constitution": 9,
        "intelligence": 9,
        "wisdom": 13,
        "charisma": 17,
    },
    ClassName.RANGER: {
        "strength": 13,
        "dexterity": 6,
        "constitution": 14,
        "intelligence": 13,
        "wisdom": 14,
        "charisma": 6,
    },
    ClassName.THIEF: {
        "strength": 6,
        "dexterity": 9,
        "constitution": 6,
        "intelligence": 6,
        "wisdom": None,
        "charisma": 6,
    },
}

# Prime requisites: list of ability names (multi-attribute uses min())
# Classes with no prime requisite have empty list
CLASS_PRIME_REQUISITES: dict[ClassName, list[str]] = {
    ClassName.PALADIN: ["strength", "wisdom"],
    ClassName.RANGER: ["strength", "intelligence", "wisdom"],
    ClassName.DRUID: ["wisdom", "charisma"],
    ClassName.FIGHTER: ["strength"],
    ClassName.CLERIC: ["wisdom"],
    ClassName.MAGIC_USER: ["intelligence"],
    ClassName.THIEF: ["dexterity"],
    ClassName.ASSASSIN: [],
    ClassName.ILLUSIONIST: [],
    ClassName.MONK: [],
}

# Priority order for class selection (higher = preferred on tie)
CLASS_PRIORITY: list[ClassName] = [
    ClassName.PALADIN,
    ClassName.RANGER,
    ClassName.DRUID,
    ClassName.FIGHTER,
    ClassName.CLERIC,
    ClassName.MAGIC_USER,
    ClassName.THIEF,
    ClassName.MONK,
    ClassName.ILLUSIONIST,
    ClassName.ASSASSIN,
]

# Hit die per class
CLASS_HIT_DIE: dict[ClassName, int] = {
    ClassName.ASSASSIN: 6,
    ClassName.CLERIC: 8,
    ClassName.DRUID: 8,
    ClassName.FIGHTER: 10,
    ClassName.ILLUSIONIST: 4,
    ClassName.MAGIC_USER: 4,
    ClassName.MONK: 4,
    ClassName.PALADIN: 10,
    ClassName.RANGER: 8,
    ClassName.THIEF: 6,
}

# Number of hit dice at level 1 (Rangers and Monks get 2)
CLASS_HIT_DICE_COUNT: dict[ClassName, int] = {
    ClassName.ASSASSIN: 1,
    ClassName.CLERIC: 1,
    ClassName.DRUID: 1,
    ClassName.FIGHTER: 1,
    ClassName.ILLUSIONIST: 1,
    ClassName.MAGIC_USER: 1,
    ClassName.MONK: 2,
    ClassName.PALADIN: 1,
    ClassName.RANGER: 2,
    ClassName.THIEF: 1,
}

# Starting gold formulas: (num_dice, die_sides, multiplier)
CLASS_STARTING_GOLD: dict[ClassName, tuple[int, int, int]] = {
    ClassName.ASSASSIN: (2, 6, 10),
    ClassName.CLERIC: (3, 6, 10),
    ClassName.DRUID: (3, 6, 10),
    ClassName.FIGHTER: (5, 4, 10),
    ClassName.ILLUSIONIST: (2, 4, 10),
    ClassName.MAGIC_USER: (2, 4, 10),
    ClassName.MONK: (5, 4, 1),
    ClassName.PALADIN: (5, 4, 10),
    ClassName.RANGER: (5, 4, 10),
    ClassName.THIEF: (2, 6, 10),
}

# Permitted alignments per class
CLASS_ALIGNMENTS: dict[ClassName, list[Alignment]] = {
    ClassName.ASSASSIN: [Alignment.LE, Alignment.NE, Alignment.CE],
    ClassName.CLERIC: list(Alignment),
    ClassName.DRUID: [Alignment.TN],
    ClassName.FIGHTER: list(Alignment),
    ClassName.ILLUSIONIST: list(Alignment),
    ClassName.MAGIC_USER: list(Alignment),
    ClassName.MONK: [Alignment.LG, Alignment.LN, Alignment.LE],
    ClassName.PALADIN: [Alignment.LG],
    ClassName.RANGER: [Alignment.LG, Alignment.NG, Alignment.CG],
    ClassName.THIEF: [
        Alignment.LN,
        Alignment.TN,
        Alignment.CN,
        Alignment.LE,
        Alignment.NE,
        Alignment.CE,
    ],
}

# Weapon proficiency slots at level 1
CLASS_PROFICIENCY_SLOTS: dict[ClassName, int] = {
    ClassName.ASSASSIN: 3,
    ClassName.CLERIC: 2,
    ClassName.DRUID: 2,
    ClassName.FIGHTER: 4,
    ClassName.ILLUSIONIST: 1,
    ClassName.MAGIC_USER: 1,
    ClassName.MONK: 1,
    ClassName.PALADIN: 3,
    ClassName.RANGER: 3,
    ClassName.THIEF: 2,
}

# Armor restrictions: list of allowed armor names (empty = no armor)
CLASS_ARMOR_ALLOWED: dict[ClassName, list[str]] = {
    ClassName.ASSASSIN: ["Leather", "Studded Leather"],
    ClassName.CLERIC: [
        "Leather",
        "Padded",
        "Studded Leather",
        "Ring Mail",
        "Scale/Lamellar",
        "Chain Mail",
        "Splint",
        "Banded",
        "Plate Mail",
    ],
    ClassName.DRUID: ["Leather"],
    ClassName.FIGHTER: [
        "Leather",
        "Padded",
        "Studded Leather",
        "Ring Mail",
        "Scale/Lamellar",
        "Chain Mail",
        "Splint",
        "Banded",
        "Plate Mail",
    ],
    ClassName.ILLUSIONIST: [],
    ClassName.MAGIC_USER: [],
    ClassName.MONK: [],
    ClassName.PALADIN: [
        "Leather",
        "Padded",
        "Studded Leather",
        "Ring Mail",
        "Scale/Lamellar",
        "Chain Mail",
        "Splint",
        "Banded",
        "Plate Mail",
    ],
    ClassName.RANGER: [
        "Leather",
        "Padded",
        "Studded Leather",
        "Ring Mail",
        "Scale/Lamellar",
        "Chain Mail",
        "Splint",
        "Banded",
        "Plate Mail",
    ],
    ClassName.THIEF: ["Leather", "Padded", "Studded Leather"],
}

# Shield allowed?
CLASS_SHIELD_ALLOWED: dict[ClassName, bool] = {
    ClassName.ASSASSIN: True,
    ClassName.CLERIC: True,
    ClassName.DRUID: True,  # wooden only
    ClassName.FIGHTER: True,
    ClassName.ILLUSIONIST: False,
    ClassName.MAGIC_USER: False,
    ClassName.MONK: False,
    ClassName.PALADIN: True,
    ClassName.RANGER: True,
    ClassName.THIEF: False,
}

# Weapons allowed per class (list of weapon names)
CLASS_WEAPONS_ALLOWED: dict[ClassName, list[str] | None] = {
    ClassName.ASSASSIN: None,  # None = any
    ClassName.CLERIC: [
        "Club",
        "Flail, heavy",
        "Flail, light",
        "Warhammer, heavy",
        "Warhammer, light",
        "Mace, heavy",
        "Mace, light",
        "Staff",
        "Torch",
    ],
    ClassName.DRUID: [
        "Club",
        "Dagger",
        "Dart",
        "Warhammer, light",
        "Sword, scimitar",
        "Sling",
        "Spear",
        "Staff",
        "Torch",
    ],
    ClassName.FIGHTER: None,
    ClassName.ILLUSIONIST: ["Dagger", "Dart", "Staff"],
    ClassName.MAGIC_USER: ["Dagger", "Dart", "Staff"],
    ClassName.MONK: [
        "Club",
        "Crossbow, heavy",
        "Crossbow, light",
        "Dagger",
        "Axe, hand",
        "Javelin",
        "Pole arm",
        "Spear",
        "Staff",
    ],
    ClassName.PALADIN: None,
    ClassName.RANGER: None,
    ClassName.THIEF: [
        "Club",
        "Dagger",
        "Dart",
        "Sling",
        "Sword, long",
        "Sword, short",
        "Sword, broad",
        "Sword, scimitar",
        "Torch",
    ],
}

# THAC0 and BTHB at level 1
CLASS_THAC0: dict[ClassName, tuple[int, int]] = {
    ClassName.ASSASSIN: (21, -1),
    ClassName.CLERIC: (20, 0),
    ClassName.DRUID: (20, 0),
    ClassName.FIGHTER: (20, 0),
    ClassName.ILLUSIONIST: (21, -1),
    ClassName.MAGIC_USER: (21, -1),
    ClassName.MONK: (20, 0),
    ClassName.PALADIN: (20, 0),
    ClassName.RANGER: (20, 0),
    ClassName.THIEF: (21, -1),
}

# Level 1 spell slots: (base_slots_level_1, spell_type)
CLASS_SPELL_SLOTS: dict[ClassName, tuple[int, str] | None] = {
    ClassName.CLERIC: (1, "divine"),
    ClassName.DRUID: (2, "druidic"),
    ClassName.ILLUSIONIST: (1, "phantasmal"),
    ClassName.MAGIC_USER: (1, "arcane"),
    ClassName.ASSASSIN: None,
    ClassName.FIGHTER: None,
    ClassName.MONK: None,
    ClassName.PALADIN: None,
    ClassName.RANGER: None,
    ClassName.THIEF: None,
}

# XP bonus condition: all prime requisites >= 16 → 10%
XP_BONUS_THRESHOLD = 16
XP_BONUS_PERCENT = 10
