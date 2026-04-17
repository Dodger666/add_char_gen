"""Tests for AncestrySelector."""

import pytest

from osric_character_gen.domain.ancestry_selector import AncestrySelector
from osric_character_gen.models.character import AbilityScores, AncestryName, ClassName


@pytest.fixture
def selector() -> AncestrySelector:
    return AncestrySelector()


class TestAncestrySelector:
    def test_human_eligible_for_fighter(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=12,
            dexterity=10,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        eligible = selector.get_eligible_ancestries(ClassName.FIGHTER, scores)
        assert AncestryName.HUMAN in eligible

    def test_human_eligible_for_all_classes_with_high_scores(
        self,
        selector: AncestrySelector,
    ) -> None:
        scores = AbilityScores(
            strength=16,
            dexterity=16,
            constitution=16,
            intelligence=16,
            wisdom=16,
            charisma=17,
        )
        for cls in ClassName:
            eligible = selector.get_eligible_ancestries(cls, scores)
            assert AncestryName.HUMAN in eligible

    def test_dwarf_eligible_for_fighter(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=12,
            dexterity=10,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        eligible = selector.get_eligible_ancestries(ClassName.FIGHTER, scores)
        assert AncestryName.DWARF in eligible

    def test_dwarf_not_eligible_for_magic_user(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=14,
            intelligence=14,
            wisdom=10,
            charisma=10,
        )
        eligible = selector.get_eligible_ancestries(ClassName.MAGIC_USER, scores)
        assert AncestryName.DWARF not in eligible

    def test_apply_dwarf_adjustments(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        adjusted = selector.apply_adjustments(scores, AncestryName.DWARF)
        assert adjusted.constitution == 15
        assert adjusted.charisma == 9

    def test_apply_elf_adjustments(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        adjusted = selector.apply_adjustments(scores, AncestryName.ELF)
        assert adjusted.dexterity == 11
        assert adjusted.constitution == 13

    def test_apply_human_no_adjustments(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        adjusted = selector.apply_adjustments(scores, AncestryName.HUMAN)
        assert adjusted == scores

    def test_validate_scores_within_range(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        assert selector.validate_scores(scores, AncestryName.DWARF, ClassName.FIGHTER)

    def test_validate_scores_out_of_range(self, selector: AncestrySelector) -> None:
        # Dwarf CON must be 12-19; CON=5 is out of range
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=5,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        assert not selector.validate_scores(scores, AncestryName.DWARF, ClassName.FIGHTER)

    def test_thief_prefers_halfling(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=12,
            constitution=12,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        result = selector.select_best_ancestry(ClassName.THIEF, scores)
        assert result == AncestryName.HALFLING

    def test_fighter_prefers_dwarf(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=12,
            dexterity=10,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        result = selector.select_best_ancestry(ClassName.FIGHTER, scores)
        assert result == AncestryName.DWARF

    def test_illusionist_prefers_gnome(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=16,
            constitution=10,
            intelligence=15,
            wisdom=10,
            charisma=10,
        )
        result = selector.select_best_ancestry(ClassName.ILLUSIONIST, scores)
        assert result == AncestryName.GNOME

    def test_half_orc_adjustments(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        adjusted = selector.apply_adjustments(scores, AncestryName.HALF_ORC)
        assert adjusted.strength == 11
        assert adjusted.constitution == 15
        assert adjusted.charisma == 8

    def test_exceptional_strength_preserved(self, selector: AncestrySelector) -> None:
        scores = AbilityScores(
            strength=18,
            dexterity=10,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
            exceptional_strength=55,
        )
        adjusted = selector.apply_adjustments(scores, AncestryName.HUMAN)
        assert adjusted.exceptional_strength == 55

    def test_default_to_human_when_no_eligible(self, selector: AncestrySelector) -> None:
        # Scores that pass Human but fail all non-humans
        scores = AbilityScores(
            strength=3,
            dexterity=3,
            constitution=3,
            intelligence=3,
            wisdom=9,
            charisma=6,
        )
        result = selector.select_best_ancestry(ClassName.CLERIC, scores)
        assert result == AncestryName.HUMAN
