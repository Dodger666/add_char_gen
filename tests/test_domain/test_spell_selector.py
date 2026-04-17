"""Tests for SpellSelector."""

import pytest

from osric_character_gen.data.spells import (
    CLERIC_SPELLS_LEVEL_1,
    DRUID_SPELLS_LEVEL_1,
    ILLUSIONIST_SPELLS_LEVEL_1,
    MAGIC_USER_SPELLS_LEVEL_1,
)
from osric_character_gen.domain.dice import DiceRoller
from osric_character_gen.domain.spell_selector import SpellSelector
from osric_character_gen.models.character import ClassName, SpellSlots


@pytest.fixture
def selector() -> SpellSelector:
    return SpellSelector(DiceRoller(seed=42))


class TestSpellSelector:
    def test_magic_user_gets_four_spells_in_book(self, selector: SpellSelector) -> None:
        slots = SpellSlots(level_1=1)
        memorized, spellbook = selector.select_starting_spells(ClassName.MAGIC_USER, slots)
        assert spellbook is not None
        assert len(spellbook) == 4
        assert "Read Magic" in spellbook

    def test_magic_user_memorizes_one(self, selector: SpellSelector) -> None:
        slots = SpellSlots(level_1=1)
        memorized, _ = selector.select_starting_spells(ClassName.MAGIC_USER, slots)
        assert len(memorized) == 1

    def test_magic_user_no_duplicates(self, selector: SpellSelector) -> None:
        slots = SpellSlots(level_1=1)
        _, spellbook = selector.select_starting_spells(ClassName.MAGIC_USER, slots)
        assert spellbook is not None
        assert len(spellbook) == len(set(spellbook))

    def test_magic_user_spells_from_valid_list(self, selector: SpellSelector) -> None:
        slots = SpellSlots(level_1=1)
        _, spellbook = selector.select_starting_spells(ClassName.MAGIC_USER, slots)
        assert spellbook is not None
        for spell in spellbook:
            assert spell in MAGIC_USER_SPELLS_LEVEL_1

    def test_illusionist_gets_three_spells(self, selector: SpellSelector) -> None:
        slots = SpellSlots(level_1=1)
        memorized, spellbook = selector.select_starting_spells(ClassName.ILLUSIONIST, slots)
        assert spellbook is not None
        assert len(spellbook) == 3
        for spell in spellbook:
            assert spell in ILLUSIONIST_SPELLS_LEVEL_1

    def test_cleric_has_cure_light_wounds(self, selector: SpellSelector) -> None:
        slots = SpellSlots(level_1=3)
        memorized, spellbook = selector.select_starting_spells(ClassName.CLERIC, slots)
        assert spellbook is None
        assert "Cure Light Wounds" in memorized
        assert len(memorized) == 3

    def test_cleric_spells_from_valid_list(self, selector: SpellSelector) -> None:
        slots = SpellSlots(level_1=3)
        memorized, _ = selector.select_starting_spells(ClassName.CLERIC, slots)
        for spell in memorized:
            assert spell in CLERIC_SPELLS_LEVEL_1

    def test_druid_gets_correct_count(self, selector: SpellSelector) -> None:
        slots = SpellSlots(level_1=2)
        memorized, spellbook = selector.select_starting_spells(ClassName.DRUID, slots)
        assert spellbook is None
        assert len(memorized) == 2
        for spell in memorized:
            assert spell in DRUID_SPELLS_LEVEL_1

    def test_fighter_no_spells(self, selector: SpellSelector) -> None:
        memorized, spellbook = selector.select_starting_spells(ClassName.FIGHTER, None)
        assert memorized == []
        assert spellbook is None

    def test_deterministic_with_seed(self) -> None:
        sel1 = SpellSelector(DiceRoller(seed=99))
        sel2 = SpellSelector(DiceRoller(seed=99))
        slots = SpellSlots(level_1=1)
        _, book1 = sel1.select_starting_spells(ClassName.MAGIC_USER, slots)
        _, book2 = sel2.select_starting_spells(ClassName.MAGIC_USER, slots)
        assert book1 == book2
