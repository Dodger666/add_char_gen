"""DMG Appendix P magical item tables for spur-of-the-moment party creation."""

from osric_character_gen.models.character import ClassName

# ---------------------------------------------------------------------------
# Protective Items Table
# Per-level percentage chance for each protective item type.
# Mutually exclusive armor types (plate/banded/chain) are grouped under
# "exclusive_armor" — the generator picks ONE by priority and rolls once.
# ---------------------------------------------------------------------------

PROTECTIVE_ITEMS_TABLE: dict[ClassName, dict[str, float]] = {
    ClassName.CLERIC: {
        "shield": 10,
        "exclusive_armor": {"plate": 5, "banded": 6, "chain": 8},
        "ring_of_protection": 2,
    },
    ClassName.DRUID: {
        "leather": 8,
        "ring_of_protection": 5,
    },
    ClassName.FIGHTER: {
        "shield": 10,
        "exclusive_armor": {"plate": 6, "banded": 8, "chain": 10},
    },
    ClassName.PALADIN: {
        "shield": 10,
        "exclusive_armor": {"plate": 6, "banded": 8, "chain": 10},
    },
    ClassName.RANGER: {
        "shield": 8,
        "exclusive_armor": {"plate": 5, "banded": 7, "chain": 15},
    },
    ClassName.MAGIC_USER: {
        "ring_of_protection": 15,
        "bracers": 4,
    },
    ClassName.ILLUSIONIST: {
        "ring_of_protection": 15,
        "bracers": 4,
    },
    ClassName.THIEF: {
        "leather": 10,
        "ring_of_protection": 4,
    },
    ClassName.ASSASSIN: {
        "shield": 8,
        "leather": 10,
        "ring_of_protection": 3,
    },
    ClassName.MONK: {},
}

# Priority order for mutually exclusive armor (best AC first)
EXCLUSIVE_ARMOR_PRIORITY: list[str] = ["plate", "banded", "chain"]

# Base AC values for armor types (descending, ascending)
ARMOR_BASE_AC: dict[str, tuple[int, int, int]] = {
    # name: (ac_desc, ac_asc, mundane_move_cap)
    "plate": (3, 17, 60),
    "banded": (4, 16, 90),
    "chain": (5, 15, 90),
    "leather": (8, 12, 120),
}

# Bracers base AC by bonus level
BRACERS_AC: dict[int, tuple[int, int]] = {
    1: (6, 14),  # AC 6 [14]
    2: (5, 15),  # AC 5 [15]
    3: (4, 16),  # AC 4 [16]
}

# ---------------------------------------------------------------------------
# Weapons Table
# Per-level percentage chance. Starred (*) entries are mutually exclusive.
# ---------------------------------------------------------------------------

WEAPONS_TABLE: dict[ClassName, dict[str, float | dict[str, float]]] = {
    ClassName.CLERIC: {
        "mace": 12,
    },
    ClassName.DRUID: {
        "dagger": 10,
        "scimitar": 7,
        "spear": 10,
    },
    ClassName.FIGHTER: {
        "dagger": 10,
        "bow": 1,
        "exclusive_weapon": {"sword": 10, "battle_axe": 7, "spear": 8, "bolts": 10},
    },
    ClassName.PALADIN: {
        "dagger": 10,
        "exclusive_weapon": {"sword": 10, "battle_axe": 10, "spear": 10},
    },
    ClassName.RANGER: {
        "dagger": 10,
        "bow": 5,
        "exclusive_weapon": {"sword": 9, "battle_axe": 9, "spear": 8, "bolts": 10},
    },
    ClassName.MAGIC_USER: {
        "dagger": 15,
    },
    ClassName.ILLUSIONIST: {
        "dagger": 15,
    },
    ClassName.THIEF: {
        "dagger": 12,
        "sword": 11,
    },
    ClassName.ASSASSIN: {
        "dagger": 10,
        "exclusive_weapon": {"sword": 5, "battle_axe": 5, "spear": 5, "bolts": 1},
        "mace": 5,
    },
    ClassName.MONK: {
        "dagger": 5,
        "spear": 2,
    },
}

# Priority for mutually exclusive weapons
EXCLUSIVE_WEAPON_PRIORITY: list[str] = ["sword", "battle_axe", "spear", "bolts"]

# Map weapon key → display name for the magic weapon
WEAPON_DISPLAY_NAMES: dict[str, str] = {
    "dagger": "Dagger",
    "sword": "Long Sword",
    "short_sword": "Short Sword",
    "scimitar": "Scimitar",
    "mace": "Mace",
    "battle_axe": "Battle Axe",
    "spear": "Spear",
    "bow": "Bow",
    "bolts": "Bolts",
}

# Small ancestries get short sword instead of long sword
SMALL_ANCESTRIES = {"Dwarf", "Gnome", "Halfling"}

# ---------------------------------------------------------------------------
# Potions Table
# (per_level_chance, max_potions)
# ---------------------------------------------------------------------------

POTIONS_TABLE: dict[ClassName, tuple[float, int]] = {
    ClassName.CLERIC: (6, 1),
    ClassName.DRUID: (11, 2),
    ClassName.FIGHTER: (8, 1),
    ClassName.PALADIN: (6, 1),
    ClassName.RANGER: (7, 1),
    ClassName.MAGIC_USER: (10, 3),
    ClassName.ILLUSIONIST: (10, 2),
    ClassName.THIEF: (9, 2),
    ClassName.ASSASSIN: (5, 1),
    ClassName.MONK: (0, 0),
}

POTION_TYPES: list[str] = [
    "Climbing",
    "Diminution",
    "Extra-healing",
    "Fire Resistance",
    "Flying",
    "Gaseous Form",
    "Growth",
    "Healing",
    "Invisibility",
    "Polymorph Self",
]

# Preferred potions for auto-select (chance >= 100%)
POTION_AUTO_SELECT_PRIORITY: list[str] = [
    "Healing",
    "Extra-healing",
    "Fire Resistance",
]

# ---------------------------------------------------------------------------
# Scrolls Table
# per_level_chance, has_protection, 1_spell_level_range, 3_spell_level_range
# None for spell ranges means no spell scrolls available.
# ---------------------------------------------------------------------------

SCROLLS_TABLE: dict[ClassName, dict] = {
    ClassName.CLERIC: {
        "chance": 8,
        "protection": False,
        "one_spell_range": (1, 3),
        "three_spell_range": (1, 4),
        "spell_class": "Cleric",
    },
    ClassName.DRUID: {
        "chance": 7,
        "protection": True,
        "one_spell_range": (1, 3),
        "three_spell_range": (1, 4),
        "spell_class": "Druid",
    },
    ClassName.FIGHTER: {
        "chance": 6,
        "protection": True,
        "one_spell_range": None,
        "three_spell_range": None,
        "spell_class": None,
    },
    ClassName.PALADIN: {
        "chance": 4,
        "protection": True,
        "one_spell_range": None,
        "three_spell_range": None,
        "spell_class": None,
    },
    ClassName.RANGER: {
        "chance": 5,
        "protection": True,
        "one_spell_range": None,
        "three_spell_range": None,
        "spell_class": None,
    },
    ClassName.MAGIC_USER: {
        "chance": 15,
        "protection": False,
        "one_spell_range": (1, 4),
        "three_spell_range": (1, 6),
        "spell_class": "Magic-User",
    },
    ClassName.ILLUSIONIST: {
        "chance": 12,
        "protection": False,
        "one_spell_range": (1, 3),
        "three_spell_range": (1, 4),
        "spell_class": "Illusionist",
    },
    ClassName.THIEF: {
        "chance": 6,
        "protection": True,
        "one_spell_range": (1, 3),
        "three_spell_range": (1, 4),
        "spell_class": "Magic-User",  # Thief uses MU spells
    },
    ClassName.ASSASSIN: {
        "chance": 3,
        "protection": True,
        "one_spell_range": (1, 3),
        "three_spell_range": None,
        "spell_class": "Magic-User",  # Assassin uses MU spells
    },
    ClassName.MONK: {
        "chance": 0,
        "protection": False,
        "one_spell_range": None,
        "three_spell_range": None,
        "spell_class": None,
    },
}

PROTECTION_SCROLL_TYPES: list[str] = [
    "Protection from Demons",
    "Protection from Devils",
    "Protection from Elementals",
    "Protection from Lycanthropes",
    "Protection from Magic",
    "Protection from Undead",
]

# ---------------------------------------------------------------------------
# Miscellaneous Items Table (for level 6+)
# ---------------------------------------------------------------------------

MISCELLANEOUS_ITEMS: list[str] = [
    "Ring of Feather Falling",
    "Ring of Warmth",
    "Ring of Water Walking",
    "Wand of Negation",
    "Wand of Wonder",
    "Bag of Holding (500 lb capacity)",
    "Folding Boat (small rowboat)",
    "Brooch of Shielding",
    "Cloak and Boots of Elvenkind",
    "Javelin of Lightning (pair)",
    "Javelin of Piercing (pair)",
    "Necklace of Adaptation",
    "Robe of Useful Items",
    "Rope of Climbing",
    "Trident of Warning",
    "Wings of Flying",
]

# Number of miscellaneous items by level bracket
MISC_ITEM_COUNT_BY_LEVEL: list[tuple[int, int, int]] = [
    # (min_level, max_level, item_count)
    (6, 8, 1),
    (9, 12, 2),
    (13, 16, 3),
    (17, 20, 4),
]


def get_misc_item_count(level: int) -> int:
    """Return the number of miscellaneous items for a given level."""
    if level < 6:
        return 0
    for min_lvl, max_lvl, count in MISC_ITEM_COUNT_BY_LEVEL:
        if min_lvl <= level <= max_lvl:
            return count
    return 4  # level > 20 edge case
