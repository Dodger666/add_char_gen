"""Weapon data from OSRIC 3.0 Player Guide."""

from osric_character_gen.models.character import ClassName

# Melee weapons: (name, hands, dmg_sm, dmg_l, weight, cost_gp)
MELEE_WEAPONS: list[tuple[str, int, str, str, float, float]] = [
    ("Axe, battle", 2, "1d8", "1d8", 7.0, 5.0),
    ("Axe, hand", 1, "1d6", "1d4", 5.0, 1.0),
    ("Club", 1, "1d6", "1d3", 3.0, 0.02),
    ("Dagger", 1, "1d4", "1d3", 1.0, 2.0),
    ("Flail, heavy", 2, "1d6+1", "2d4", 10.0, 3.0),
    ("Flail, light", 1, "1d4+1", "1d4+1", 4.0, 6.0),
    ("Halberd", 2, "1d10", "2d6", 18.0, 9.0),
    ("Javelin", 1, "1d6", "1d4", 2.0, 0.5),
    ("Lance", 1, "2d4+1", "3d6", 15.0, 6.0),
    ("Mace, heavy", 2, "1d6+1", "1d6", 10.0, 10.0),
    ("Mace, light", 1, "1d4+1", "1d4+1", 5.0, 4.0),
    ("Morning star", 2, "2d4", "1d6+1", 12.0, 5.0),
    ("Pick, heavy", 2, "1d6+1", "2d4", 1.0, 8.0),
    ("Pick, light", 1, "1d4+1", "1d4", 4.0, 5.0),
    ("Pole arm", 2, "1d6+1", "1d10", 8.0, 6.0),
    ("Spear", 1, "1d6", "1d8", 5.0, 1.0),
    ("Staff", 2, "1d6", "1d6", 5.0, 0.0),
    ("Sword, bastard", 2, "2d4", "2d8", 10.0, 25.0),
    ("Sword, broad", 1, "2d4", "1d6+1", 8.0, 15.0),
    ("Sword, long", 1, "1d8", "1d12", 7.0, 15.0),
    ("Sword, scimitar", 1, "1d8", "1d8", 5.0, 15.0),
    ("Sword, short", 1, "1d6", "1d8", 3.0, 8.0),
    ("Sword, two-handed", 2, "1d10", "3d6", 25.0, 30.0),
    ("Torch", 1, "1d4", "1d4", 1.0, 0.01),
    ("Trident", 2, "1d6+1", "3d4", 5.0, 4.0),
    ("Warhammer, heavy", 2, "1d6+1", "1d6", 10.0, 7.0),
    ("Warhammer, light", 1, "1d4+1", "1d4", 5.0, 1.0),
]

# Missile weapons: (name, hands, dmg_sm, dmg_l, range_ft, rof, weight, cost_gp)
MISSILE_WEAPONS: list[tuple[str, int, str, str, int, str, float, float]] = [
    ("Bow, long", 2, "1d6", "1d6", 70, "2", 12.0, 60.0),
    ("Bow, short", 2, "1d6", "1d6", 50, "2", 8.0, 15.0),
    ("Composite bow, long", 2, "1d6", "1d6", 60, "2", 8.0, 100.0),
    ("Composite bow, short", 2, "1d6", "1d6", 50, "2", 5.0, 75.0),
    ("Crossbow, heavy", 2, "1d6+1", "1d6+1", 80, "1/2", 12.0, 20.0),
    ("Crossbow, light", 2, "1d4+1", "1d4+1", 60, "1", 4.0, 12.0),
    ("Dart", 1, "1d3", "1d2", 15, "3", 0.5, 0.2),
    ("Sling", 1, "1d4+1", "1d6+1", 35, "1", 0.5, 0.5),
]

# Ammunition: (name, weight_per_dozen, cost_per_dozen)
AMMUNITION: list[tuple[str, float, float]] = [
    ("Arrow", 4.0, 2.0),
    ("Bolt, heavy", 4.0, 4.0),
    ("Bolt, light", 2.0, 2.0),
    ("Sling bullet", 4.0, 1.0),
]

# Weapon-to-ammunition mapping
WEAPON_AMMO: dict[str, str] = {
    "Bow, long": "Arrow",
    "Bow, short": "Arrow",
    "Composite bow, long": "Arrow",
    "Composite bow, short": "Arrow",
    "Crossbow, heavy": "Bolt, heavy",
    "Crossbow, light": "Bolt, light",
    "Sling": "Sling bullet",
}

# Primary weapon priority per class
WEAPON_PRIORITY: dict[ClassName, list[str]] = {
    ClassName.FIGHTER: ["Sword, long", "Sword, broad", "Mace, heavy", "Spear"],
    ClassName.PALADIN: ["Sword, long", "Sword, broad", "Mace, heavy", "Spear"],
    ClassName.RANGER: ["Sword, long", "Sword, broad", "Mace, heavy", "Spear"],
    ClassName.CLERIC: ["Mace, light", "Flail, light", "Warhammer, light", "Staff", "Club"],
    ClassName.DRUID: ["Sword, scimitar", "Spear", "Club", "Staff"],
    ClassName.ASSASSIN: ["Sword, long", "Sword, short", "Dagger"],
    ClassName.THIEF: ["Sword, short", "Dagger", "Club"],
    ClassName.MAGIC_USER: ["Dagger", "Staff"],
    ClassName.ILLUSIONIST: ["Dagger", "Staff"],
    ClassName.MONK: ["Staff", "Club", "Dagger"],
}

# Backup weapon priority (lighter/cheaper options)
BACKUP_WEAPON_PRIORITY: dict[ClassName, list[str]] = {
    ClassName.FIGHTER: ["Dagger", "Axe, hand"],
    ClassName.PALADIN: ["Dagger", "Axe, hand"],
    ClassName.RANGER: ["Dagger", "Axe, hand"],
    ClassName.CLERIC: ["Staff", "Club"],
    ClassName.DRUID: ["Club", "Staff", "Dagger"],
    ClassName.ASSASSIN: ["Dagger"],
    ClassName.THIEF: ["Dagger"],
    ClassName.MAGIC_USER: ["Staff"],
    ClassName.ILLUSIONIST: ["Staff"],
    ClassName.MONK: ["Dagger"],
}


def get_melee_weapon(name: str) -> tuple[str, int, str, str, float, float] | None:
    """Find a melee weapon by name."""
    for w in MELEE_WEAPONS:
        if w[0] == name:
            return w
    return None


def get_missile_weapon(
    name: str,
) -> tuple[str, int, str, str, int, str, float, float] | None:
    """Find a missile weapon by name."""
    for w in MISSILE_WEAPONS:
        if w[0] == name:
            return w
    return None


def get_ammo_for_weapon(weapon_name: str) -> tuple[str, float, float] | None:
    """Get ammunition info for a missile weapon."""
    ammo_name = WEAPON_AMMO.get(weapon_name)
    if ammo_name is None:
        return None
    for a in AMMUNITION:
        if a[0] == ammo_name:
            return a
    return None
