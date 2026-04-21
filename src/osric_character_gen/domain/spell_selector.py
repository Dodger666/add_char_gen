"""Spell selection logic for OSRIC 3.0 character generation."""

import math

from osric_character_gen.data.spells import (
    SPELL_LISTS,
)
from osric_character_gen.domain.dice import DiceRoller
from osric_character_gen.models.character import ClassName, SpellSlots


class SpellSelector:
    def __init__(self, roller: DiceRoller) -> None:
        self._roller = roller

    def select_starting_spells(
        self, class_name: ClassName, spell_slots: SpellSlots | None
    ) -> tuple[list[str], list[str] | None]:
        """Return (spells_memorized, spellbook_contents).
        spellbook is None for non-arcane casters."""
        if spell_slots is None:
            return [], None

        if class_name == ClassName.MAGIC_USER:
            return self._select_arcane_spells(
                class_name,
                spell_slots,
                has_spellbook=True,
                must_have_read_magic=True,
                base_spellbook_size=4,
            )
        if class_name == ClassName.ILLUSIONIST:
            return self._select_arcane_spells(
                class_name,
                spell_slots,
                has_spellbook=True,
                must_have_read_magic=False,
                base_spellbook_size=3,
            )
        if class_name == ClassName.CLERIC:
            return self._select_divine_spells(class_name, spell_slots, priority_spell="Cure Light Wounds")
        if class_name == ClassName.DRUID:
            return self._select_divine_spells(class_name, spell_slots)
        if class_name == ClassName.PALADIN:
            return self._select_divine_spells(class_name, spell_slots, priority_spell="Cure Light Wounds")
        if class_name == ClassName.RANGER:
            return self._select_ranger_spells(spell_slots)

        return [], None

    def _select_arcane_spells(
        self,
        class_name: ClassName,
        spell_slots: SpellSlots,
        *,
        has_spellbook: bool,
        must_have_read_magic: bool,
        base_spellbook_size: int,
    ) -> tuple[list[str], list[str] | None]:
        """Select spells for arcane casters (MU, Illusionist)."""
        cls_key = class_name.value
        spell_lists = SPELL_LISTS.get(cls_key, {})
        all_memorized: list[str] = []
        all_spellbook: list[str] = []

        for spell_level in range(1, 8):
            slot_count = getattr(spell_slots, f"level_{spell_level}", 0)
            if slot_count <= 0:
                continue
            pool = spell_lists.get(spell_level, [])
            if not pool:
                continue

            if spell_level == 1:
                # Level 1: spellbook has base_spellbook_size or more
                spellbook_size = max(base_spellbook_size, math.ceil(slot_count * 1.5))
                spellbook_size = min(spellbook_size, len(pool))
                if must_have_read_magic and "Read Magic" in pool:
                    other_pool = [s for s in pool if s != "Read Magic"]
                    others = self._roller.sample(other_pool, min(spellbook_size - 1, len(other_pool)))
                    level_book = ["Read Magic"] + sorted(others)
                else:
                    level_book = sorted(self._roller.sample(pool, spellbook_size))
            else:
                spellbook_size = min(math.ceil(slot_count * 1.5), len(pool))
                level_book = sorted(self._roller.sample(pool, spellbook_size))

            all_spellbook.extend(level_book)
            memorized = level_book[:slot_count]
            all_memorized.extend(memorized)

        return all_memorized, all_spellbook if has_spellbook else None

    def _select_divine_spells(
        self,
        class_name: ClassName,
        spell_slots: SpellSlots,
        priority_spell: str | None = None,
    ) -> tuple[list[str], None]:
        """Select spells for divine casters (Cleric, Druid, Paladin)."""
        cls_key = class_name.value
        spell_lists = SPELL_LISTS.get(cls_key, {})
        all_memorized: list[str] = []

        for spell_level in range(1, 8):
            slot_count = getattr(spell_slots, f"level_{spell_level}", 0)
            if slot_count <= 0:
                continue
            pool = spell_lists.get(spell_level, [])
            if not pool:
                continue

            if spell_level == 1 and priority_spell and priority_spell in pool:
                memorized = [priority_spell]
                remaining = slot_count - 1
                if remaining > 0:
                    other_pool = [s for s in pool if s != priority_spell]
                    extra = self._roller.sample(other_pool, min(remaining, len(other_pool)))
                    memorized.extend(sorted(extra))
            else:
                count = min(slot_count, len(pool))
                memorized = sorted(self._roller.sample(pool, count))

            all_memorized.extend(memorized)

        return all_memorized, None

    def _select_ranger_spells(self, spell_slots: SpellSlots) -> tuple[list[str], None]:
        """Select spells for Ranger (druid + MU spell lists)."""
        druid_lists = SPELL_LISTS.get("Druid", {})
        all_memorized: list[str] = []

        # Ranger uses druid spells for its primary slots
        for spell_level in range(1, 8):
            slot_count = getattr(spell_slots, f"level_{spell_level}", 0)
            if slot_count <= 0:
                continue
            pool = druid_lists.get(spell_level, [])
            if not pool:
                continue
            count = min(slot_count, len(pool))
            memorized = sorted(self._roller.sample(pool, count))
            all_memorized.extend(memorized)

        return all_memorized, None
