"""Thief skill tables from OSRIC 3.0 Player Guide."""

from osric_character_gen.models.character import AncestryName

# Base thief skills at level 1
BASE_THIEF_SKILLS: dict[str, int] = {
    "climb": 85,
    "hide": 10,
    "listen": 10,
    "pick_locks": 25,
    "pick_pockets": 30,
    "read_languages": 1,
    "move_quietly": 15,
    "traps": 20,
}

# DEX adjustments to thief skills
# {dex: {skill: adjustment}}
DEX_THIEF_ADJUSTMENTS: dict[int, dict[str, int]] = {
    9: {"hide": -10, "pick_locks": -10, "pick_pockets": -15, "move_quietly": -20, "traps": -15},
    10: {"hide": -5, "pick_locks": -5, "pick_pockets": -10, "move_quietly": -15, "traps": -10},
    11: {"pick_pockets": -5, "move_quietly": -10, "traps": -5},
    12: {"move_quietly": -5},
    # 13-15: no adjustments
    16: {"pick_locks": 5},
    17: {"hide": 5, "pick_locks": 10, "pick_pockets": 5, "move_quietly": 5, "traps": 5},
    18: {"hide": 10, "pick_locks": 15, "pick_pockets": 10, "move_quietly": 10, "traps": 10},
    19: {"hide": 15, "pick_locks": 20, "pick_pockets": 15, "move_quietly": 15, "traps": 15},
}

# Ancestry adjustments to thief skills
ANCESTRY_THIEF_ADJUSTMENTS: dict[AncestryName, dict[str, int]] = {
    AncestryName.DWARF: {
        "climb": -10,
        "pick_locks": 15,
        "move_quietly": -5,
        "traps": 15,
        "read_languages": -5,
    },
    AncestryName.ELF: {
        "climb": -5,
        "hide": 10,
        "listen": 5,
        "pick_locks": -5,
        "pick_pockets": 5,
        "move_quietly": 5,
        "traps": 5,
        "read_languages": 10,
    },
    AncestryName.GNOME: {
        "climb": -15,
        "listen": 5,
        "pick_locks": 10,
    },
    AncestryName.HALF_ELF: {
        "hide": 5,
        "pick_pockets": 10,
    },
    AncestryName.HALFLING: {
        "climb": -15,
        "hide": 15,
        "listen": 5,
        "pick_pockets": 5,
        "move_quietly": 15,
        "read_languages": -5,
    },
    AncestryName.HALF_ORC: {
        "climb": 5,
        "listen": 5,
        "pick_locks": 5,
        "pick_pockets": -5,
        "traps": 5,
        "read_languages": -10,
    },
    AncestryName.HUMAN: {
        "climb": 5,
        "pick_locks": 5,
    },
}

# Skills that monks do NOT get
MONK_EXCLUDED_SKILLS = {"pick_pockets", "read_languages"}
