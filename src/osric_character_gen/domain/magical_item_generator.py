"""Magical item generation per DMG Appendix P."""

from osric_character_gen.data.magical_items import (
    ARMOR_BASE_AC,
    BRACERS_AC,
    EXCLUSIVE_ARMOR_PRIORITY,
    EXCLUSIVE_WEAPON_PRIORITY,
    MISCELLANEOUS_ITEMS,
    POTION_AUTO_SELECT_PRIORITY,
    POTION_TYPES,
    POTIONS_TABLE,
    PROTECTION_SCROLL_TYPES,
    PROTECTIVE_ITEMS_TABLE,
    SCROLLS_TABLE,
    SMALL_ANCESTRIES,
    WEAPON_DISPLAY_NAMES,
    WEAPONS_TABLE,
    get_misc_item_count,
)
from osric_character_gen.data.spells import SPELL_LISTS
from osric_character_gen.domain.dice import DiceRoller
from osric_character_gen.models.character import AncestryName, ClassName, MagicalItem


class MagicalItemGenerator:
    def __init__(self, roller: DiceRoller) -> None:
        self._roller = roller

    def generate_magical_items(
        self,
        class_name: ClassName,
        level: int,
        ancestry: AncestryName,
    ) -> list[MagicalItem]:
        if level < 2:
            return []

        items: list[MagicalItem] = []
        items.extend(self._roll_protective_items(class_name, level))
        items.extend(self._roll_weapons(class_name, level, ancestry))
        items.extend(self._roll_potions(class_name, level))
        items.extend(self._roll_scrolls(class_name, level))
        items.extend(self._roll_miscellaneous(level))
        return items

    # ------------------------------------------------------------------
    # Enhancement logic (shared by armor, shields, weapons)
    # ------------------------------------------------------------------

    def _roll_enhancement(self, level: int, effective_chance: float) -> int:
        """Roll for +1/+2/+3 enhancement. Returns bonus level."""
        above_avg_chance = level
        if effective_chance > 90:
            above_avg_chance += effective_chance - 90
        roll = self._roller.roll_percentile()
        if roll <= above_avg_chance:
            # Check for +3
            exceptional_chance = level
            roll2 = self._roller.roll_percentile()
            if roll2 <= exceptional_chance:
                return 3
            return 2
        return 1

    def _check_item(self, per_level_pct: float, level: int) -> bool:
        """Roll d100 against effective chance. Auto-success if >= 100."""
        effective = per_level_pct * level
        if effective >= 100:
            return True
        return self._roller.roll_percentile() <= effective

    # ------------------------------------------------------------------
    # Protective items
    # ------------------------------------------------------------------

    def _roll_protective_items(self, class_name: ClassName, level: int) -> list[MagicalItem]:
        items: list[MagicalItem] = []
        table = PROTECTIVE_ITEMS_TABLE.get(class_name, {})

        for key, value in table.items():
            if key == "exclusive_armor":
                item = self._roll_exclusive_armor(value, level)
                if item:
                    items.append(item)
            elif key == "shield":
                if self._check_item(value, level):
                    bonus = self._roll_enhancement(level, value * level)
                    items.append(
                        MagicalItem(
                            name=f"Shield +{bonus}",
                            item_type="shield",
                            bonus=bonus,
                            equipped=True,
                            replaces_mundane="Shield",
                        )
                    )
            elif key == "leather":
                if self._check_item(value, level):
                    bonus = self._roll_enhancement(level, value * level)
                    base_ac_d, base_ac_a, _ = ARMOR_BASE_AC["leather"]
                    items.append(
                        MagicalItem(
                            name=f"Leather Armor +{bonus}",
                            item_type="armor",
                            bonus=bonus,
                            properties={"ac_desc": base_ac_d - bonus, "ac_asc": base_ac_a + bonus},
                            equipped=True,
                            replaces_mundane="Leather Armor",
                        )
                    )
            elif key == "ring_of_protection":
                if self._check_item(value, level):
                    bonus = self._roll_enhancement(level, value * level)
                    items.append(
                        MagicalItem(
                            name=f"Ring of Protection +{bonus}",
                            item_type="ring",
                            bonus=bonus,
                            properties={"save_bonus": bonus},
                            equipped=True,
                        )
                    )
            elif key == "bracers":
                if self._check_item(value, level):
                    bonus = self._roll_enhancement(level, value * level)
                    bonus = min(bonus, 3)
                    ac_desc, ac_asc = BRACERS_AC[bonus]
                    items.append(
                        MagicalItem(
                            name=f"Bracers of Defence AC {ac_desc} [{ac_asc}]",
                            item_type="bracers",
                            bonus=bonus,
                            properties={"ac_desc": ac_desc, "ac_asc": ac_asc},
                            equipped=True,
                        )
                    )

        return items

    def _roll_exclusive_armor(self, armor_dict: dict[str, float], level: int) -> MagicalItem | None:
        """Pick best armor by priority, roll once."""
        for armor_type in EXCLUSIVE_ARMOR_PRIORITY:
            if armor_type in armor_dict:
                pct = armor_dict[armor_type]
                if self._check_item(pct, level):
                    bonus = self._roll_enhancement(level, pct * level)
                    base_ac_d, base_ac_a, _ = ARMOR_BASE_AC[armor_type]
                    display = armor_type.replace("_", " ").title() + " Mail"
                    if armor_type == "plate":
                        display = "Plate Mail"
                    elif armor_type == "banded":
                        display = "Banded Mail"
                    elif armor_type == "chain":
                        display = "Chain Mail"
                    return MagicalItem(
                        name=f"{display} +{bonus}",
                        item_type="armor",
                        bonus=bonus,
                        properties={"ac_desc": base_ac_d - bonus, "ac_asc": base_ac_a + bonus},
                        equipped=True,
                        replaces_mundane=display,
                    )
                # Failed the roll — no fallback
                return None
        return None

    # ------------------------------------------------------------------
    # Weapons
    # ------------------------------------------------------------------

    def _roll_weapons(self, class_name: ClassName, level: int, ancestry: AncestryName) -> list[MagicalItem]:
        items: list[MagicalItem] = []
        table = WEAPONS_TABLE.get(class_name, {})
        is_small = ancestry.value in SMALL_ANCESTRIES

        for key, value in table.items():
            if key == "exclusive_weapon":
                item = self._roll_exclusive_weapon(value, level, is_small, class_name)
                if item:
                    if isinstance(item, list):
                        items.extend(item)
                    else:
                        items.append(item)
            elif key == "sword":
                if self._check_item(value, level):
                    bonus = self._roll_enhancement(level, value * level)
                    wpn_name = self._sword_name(is_small, class_name)
                    items.append(
                        MagicalItem(
                            name=f"{wpn_name} +{bonus}",
                            item_type="weapon",
                            bonus=bonus,
                            equipped=True,
                            replaces_mundane=wpn_name,
                        )
                    )
            elif key == "scimitar":
                if self._check_item(value, level):
                    bonus = self._roll_enhancement(level, value * level)
                    items.append(
                        MagicalItem(
                            name=f"Scimitar +{bonus}",
                            item_type="weapon",
                            bonus=bonus,
                            equipped=True,
                            replaces_mundane="Scimitar",
                        )
                    )
            else:
                display = WEAPON_DISPLAY_NAMES.get(key, key.title())
                if self._check_item(value, level):
                    bonus = self._roll_enhancement(level, value * level)
                    if key == "bow":
                        items.append(
                            MagicalItem(
                                name=f"Bow +{bonus}",
                                item_type="weapon",
                                bonus=bonus,
                                equipped=True,
                                replaces_mundane="Bow",
                            )
                        )
                        items.append(
                            MagicalItem(
                                name="Arrows (20)",
                                item_type="ammunition",
                                bonus=None,
                                equipped=False,
                            )
                        )
                    else:
                        items.append(
                            MagicalItem(
                                name=f"{display} +{bonus}",
                                item_type="weapon",
                                bonus=bonus,
                                equipped=True,
                                replaces_mundane=display,
                            )
                        )

        return items

    def _roll_exclusive_weapon(
        self,
        wpn_dict: dict[str, float],
        level: int,
        is_small: bool,
        class_name: ClassName,
    ) -> MagicalItem | list[MagicalItem] | None:
        for wpn_type in EXCLUSIVE_WEAPON_PRIORITY:
            if wpn_type in wpn_dict:
                pct = wpn_dict[wpn_type]
                if self._check_item(pct, level):
                    bonus = self._roll_enhancement(level, pct * level)
                    if wpn_type == "sword":
                        wpn_name = self._sword_name(is_small, class_name)
                        return MagicalItem(
                            name=f"{wpn_name} +{bonus}",
                            item_type="weapon",
                            bonus=bonus,
                            equipped=True,
                            replaces_mundane=wpn_name,
                        )
                    elif wpn_type == "bolts":
                        # Bolts are always +2 base; +3 → Crossbow of Speed + 30 bolts
                        if bonus >= 3:
                            return [
                                MagicalItem(
                                    name="Crossbow of Speed",
                                    item_type="weapon",
                                    bonus=3,
                                    equipped=True,
                                    replaces_mundane="Crossbow",
                                ),
                                MagicalItem(
                                    name="Bolts +2 (30)",
                                    item_type="ammunition",
                                    bonus=2,
                                    equipped=False,
                                ),
                            ]
                        return MagicalItem(
                            name="Bolts +2 (15)",
                            item_type="ammunition",
                            bonus=2,
                            equipped=False,
                        )
                    else:
                        display = WEAPON_DISPLAY_NAMES.get(wpn_type, wpn_type.title())
                        return MagicalItem(
                            name=f"{display} +{bonus}",
                            item_type="weapon",
                            bonus=bonus,
                            equipped=True,
                            replaces_mundane=display,
                        )
                return None
        return None

    def _sword_name(self, is_small: bool, class_name: ClassName) -> str:
        if class_name == ClassName.DRUID:
            return "Scimitar"
        if is_small:
            return "Short Sword"
        return "Long Sword"

    # ------------------------------------------------------------------
    # Potions
    # ------------------------------------------------------------------

    def _roll_potions(self, class_name: ClassName, level: int) -> list[MagicalItem]:
        per_level, max_potions = POTIONS_TABLE.get(class_name, (0, 0))
        if max_potions == 0 or per_level == 0:
            return []

        items: list[MagicalItem] = []
        effective = per_level * level

        for _ in range(max_potions):
            if effective >= 100:
                # Auto-select from priority list
                for pname in POTION_AUTO_SELECT_PRIORITY:
                    already = {i.name for i in items}
                    if f"Potion of {pname}" not in already:
                        items.append(
                            MagicalItem(
                                name=f"Potion of {pname}",
                                item_type="potion",
                                equipped=False,
                            )
                        )
                        break
                else:
                    # All priority potions taken, random
                    idx = self._roller.roll(10) - 1
                    items.append(
                        MagicalItem(
                            name=f"Potion of {POTION_TYPES[idx]}",
                            item_type="potion",
                            equipped=False,
                        )
                    )
            elif self._roller.roll_percentile() <= effective:
                idx = self._roller.roll(10) - 1
                items.append(
                    MagicalItem(
                        name=f"Potion of {POTION_TYPES[idx]}",
                        item_type="potion",
                        equipped=False,
                    )
                )
            else:
                break  # Failed roll, stop trying additional potions

        return items

    # ------------------------------------------------------------------
    # Scrolls
    # ------------------------------------------------------------------

    def _roll_scrolls(self, class_name: ClassName, level: int) -> list[MagicalItem]:
        entry = SCROLLS_TABLE.get(class_name)
        if not entry or entry["chance"] == 0:
            return []

        pct = entry["chance"]
        effective = pct * level
        if effective < 100 and self._roller.roll_percentile() > effective:
            return []

        # Determine scroll type
        has_protection = entry["protection"]
        has_spells = entry["one_spell_range"] is not None
        spell_class = entry["spell_class"]

        if has_protection and not has_spells:
            # Fighter, Paladin, Ranger: protection scroll only
            scroll_type = self._roller.choice(PROTECTION_SCROLL_TYPES)
            return [
                MagicalItem(
                    name=f"Scroll of {scroll_type}",
                    item_type="scroll",
                    equipped=False,
                    properties={"protection_type": scroll_type},
                )
            ]

        if has_spells and not has_protection:
            # Pure casters: spell scroll only
            return self._generate_spell_scroll(entry, spell_class)

        # Has both options (Druid, Thief, Assassin)
        if self._roller.roll_percentile() <= 50:
            scroll_type = self._roller.choice(PROTECTION_SCROLL_TYPES)
            return [
                MagicalItem(
                    name=f"Scroll of {scroll_type}",
                    item_type="scroll",
                    equipped=False,
                    properties={"protection_type": scroll_type},
                )
            ]
        return self._generate_spell_scroll(entry, spell_class)

    def _generate_spell_scroll(self, entry: dict, spell_class: str) -> list[MagicalItem]:
        """Generate a 1-spell or 3-spell scroll."""
        if self._roller.roll_percentile() <= 50:
            # 1 spell
            spell_range = entry["one_spell_range"]
            if spell_range is None:
                return []
            spells = self._pick_spells(spell_class, spell_range, 1)
            return [
                MagicalItem(
                    name=f"Spell Scroll ({', '.join(spells)})",
                    item_type="scroll",
                    equipped=False,
                    properties={"spells": spells, "spell_class": spell_class},
                )
            ]
        # 3 spells
        spell_range = entry["three_spell_range"]
        if spell_range is None:
            # Fallback to 1 spell if 3-spell not available
            spell_range = entry["one_spell_range"]
            if spell_range is None:
                return []
            spells = self._pick_spells(spell_class, spell_range, 1)
            return [
                MagicalItem(
                    name=f"Spell Scroll ({', '.join(spells)})",
                    item_type="scroll",
                    equipped=False,
                    properties={"spells": spells, "spell_class": spell_class},
                )
            ]
        spells = self._pick_spells(spell_class, spell_range, 3)
        return [
            MagicalItem(
                name=f"Spell Scroll ({', '.join(spells)})",
                item_type="scroll",
                equipped=False,
                properties={"spells": spells, "spell_class": spell_class},
            )
        ]

    def _pick_spells(self, spell_class: str, level_range: tuple[int, int], count: int) -> list[str]:
        """Pick random spells from the class list within level range."""
        spells: list[str] = []
        class_lists = SPELL_LISTS.get(spell_class, {})
        min_lvl, max_lvl = level_range

        for _ in range(count):
            spell_level = self._roller.roll(max_lvl - min_lvl + 1) + min_lvl - 1
            available = class_lists.get(spell_level, [])
            if available:
                spell = self._roller.choice(available)
                spells.append(spell)
            else:
                # Fallback: try level 1
                fallback = class_lists.get(1, [])
                if fallback:
                    spells.append(self._roller.choice(fallback))

        return spells

    # ------------------------------------------------------------------
    # Miscellaneous items
    # ------------------------------------------------------------------

    def _roll_miscellaneous(self, level: int) -> list[MagicalItem]:
        count = get_misc_item_count(level)
        if count == 0:
            return []

        chosen: list[str] = []
        available = list(MISCELLANEOUS_ITEMS)
        for _ in range(count):
            if not available:
                break
            idx = self._roller.roll(len(available)) - 1
            item_name = available.pop(idx)
            chosen.append(item_name)

        return [MagicalItem(name=name, item_type="miscellaneous", equipped=False) for name in chosen]
