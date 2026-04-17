"""Spell selection logic for OSRIC 3.0 character generation."""

from osric_character_gen.data.spells import (
    CLERIC_SPELLS_LEVEL_1,
    DRUID_SPELLS_LEVEL_1,
    ILLUSIONIST_SPELLS_LEVEL_1,
    MAGIC_USER_SPELLS_LEVEL_1,
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
            return self._select_magic_user_spells(spell_slots)
        if class_name == ClassName.ILLUSIONIST:
            return self._select_illusionist_spells(spell_slots)
        if class_name == ClassName.CLERIC:
            return self._select_cleric_spells(spell_slots)
        if class_name == ClassName.DRUID:
            return self._select_druid_spells(spell_slots)

        return [], None

    def _select_magic_user_spells(self, spell_slots: SpellSlots) -> tuple[list[str], list[str]]:
        """MU starts with 4 spells in spellbook. Read Magic always included."""
        pool = [s for s in MAGIC_USER_SPELLS_LEVEL_1 if s != "Read Magic"]
        other_spells = self._roller.sample(pool, 3)
        spellbook = ["Read Magic"] + sorted(other_spells)

        # Memorize up to level_1 slots
        memorized = spellbook[: spell_slots.level_1]
        return memorized, spellbook

    def _select_illusionist_spells(self, spell_slots: SpellSlots) -> tuple[list[str], list[str]]:
        """Illusionist starts with 3 random spells in spellbook."""
        spellbook = sorted(self._roller.sample(ILLUSIONIST_SPELLS_LEVEL_1, 3))
        memorized = spellbook[: spell_slots.level_1]
        return memorized, spellbook

    def _select_cleric_spells(self, spell_slots: SpellSlots) -> tuple[list[str], None]:
        """Cleric memorizes from all divine spells. CLW first."""
        total_slots = spell_slots.level_1
        memorized = ["Cure Light Wounds"]
        remaining = total_slots - 1

        if remaining > 0:
            pool = [s for s in CLERIC_SPELLS_LEVEL_1 if s != "Cure Light Wounds"]
            extra = self._roller.sample(pool, min(remaining, len(pool)))
            memorized.extend(sorted(extra))

        return memorized, None

    def _select_druid_spells(self, spell_slots: SpellSlots) -> tuple[list[str], None]:
        """Druid memorizes from all druidic spells."""
        total_slots = spell_slots.level_1
        memorized = sorted(self._roller.sample(DRUID_SPELLS_LEVEL_1, min(total_slots, len(DRUID_SPELLS_LEVEL_1))))
        return memorized, None
