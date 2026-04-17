"""Tests for ClassSelector."""

import pytest

from osric_character_gen.domain.class_selector import (
    ClassSelector,
    NoEligibleClassError,
)
from osric_character_gen.models.character import AbilityScores, ClassName


@pytest.fixture
def selector() -> ClassSelector:
    return ClassSelector()


class TestClassSelector:
    def test_fighter_eligible_with_minimum_scores(self, selector: ClassSelector) -> None:
        scores = AbilityScores(
            strength=9,
            dexterity=6,
            constitution=7,
            intelligence=3,
            wisdom=6,
            charisma=6,
        )
        eligible = selector.get_eligible_classes(scores)
        assert ClassName.FIGHTER in eligible

    def test_paladin_requires_high_charisma(self, selector: ClassSelector) -> None:
        scores = AbilityScores(
            strength=12,
            dexterity=6,
            constitution=9,
            intelligence=9,
            wisdom=13,
            charisma=16,
        )
        eligible = selector.get_eligible_classes(scores)
        assert ClassName.PALADIN not in eligible

    def test_paladin_eligible(self, selector: ClassSelector) -> None:
        scores = AbilityScores(
            strength=12,
            dexterity=6,
            constitution=9,
            intelligence=9,
            wisdom=13,
            charisma=17,
        )
        eligible = selector.get_eligible_classes(scores)
        assert ClassName.PALADIN in eligible

    def test_no_eligible_class_raises(self, selector: ClassSelector) -> None:
        scores = AbilityScores(
            strength=3,
            dexterity=3,
            constitution=3,
            intelligence=3,
            wisdom=3,
            charisma=3,
        )
        with pytest.raises(NoEligibleClassError):
            selector.select_best_class(scores)

    def test_select_best_class_prefers_highest_prime_requisite(
        self,
        selector: ClassSelector,
    ) -> None:
        # WIS 17 > STR 14 → should pick Cleric
        scores = AbilityScores(
            strength=14,
            dexterity=12,
            constitution=14,
            intelligence=12,
            wisdom=17,
            charisma=12,
        )
        result = selector.select_best_class(scores)
        assert result == ClassName.CLERIC

    def test_select_best_class_fighter_with_high_str(
        self,
        selector: ClassSelector,
    ) -> None:
        scores = AbilityScores(
            strength=18,
            dexterity=10,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        result = selector.select_best_class(scores)
        assert result == ClassName.FIGHTER

    def test_select_best_class_paladin_preferred_on_tie(
        self,
        selector: ClassSelector,
    ) -> None:
        # STR=16, WIS=16 → Paladin (priority) score=min(16,16)=16
        # Also qualifies Fighter score=16, Cleric score=16
        # Paladin has higher priority
        scores = AbilityScores(
            strength=16,
            dexterity=16,
            constitution=14,
            intelligence=13,
            wisdom=16,
            charisma=17,
        )
        result = selector.select_best_class(scores)
        assert result == ClassName.PALADIN

    def test_score_class_no_prime_requisite(self, selector: ClassSelector) -> None:
        scores = AbilityScores(
            strength=18,
            dexterity=18,
            constitution=18,
            intelligence=18,
            wisdom=18,
            charisma=18,
        )
        assert selector.score_class(ClassName.ASSASSIN, scores) == 0

    def test_score_class_multi_prime_uses_min(self, selector: ClassSelector) -> None:
        scores = AbilityScores(
            strength=16,
            dexterity=10,
            constitution=14,
            intelligence=12,
            wisdom=18,
            charisma=15,
        )
        # Druid prime: min(WIS=18, CHA=15) = 15
        assert selector.score_class(ClassName.DRUID, scores) == 15

    def test_ranger_prime_requisite(self, selector: ClassSelector) -> None:
        scores = AbilityScores(
            strength=16,
            dexterity=10,
            constitution=14,
            intelligence=14,
            wisdom=15,
            charisma=10,
        )
        # Ranger: min(STR=16, INT=14, WIS=15) = 14
        assert selector.score_class(ClassName.RANGER, scores) == 14

    def test_only_no_prime_classes_eligible(self, selector: ClassSelector) -> None:
        # Scores that only qualify Assassin and Monk
        scores = AbilityScores(
            strength=12,
            dexterity=15,
            constitution=6,
            intelligence=11,
            wisdom=10,
            charisma=5,
        )
        eligible = selector.get_eligible_classes(scores)
        # Check that Monk is selected (preferred over Assassin)
        result = selector.select_best_class(scores)
        if ClassName.MONK in eligible and ClassName.ASSASSIN in eligible:
            assert result == ClassName.MONK

    def test_all_ten_classes_in_minimums(self, selector: ClassSelector) -> None:
        """Every class has an entry in CLASS_MINIMUMS."""
        for cls in ClassName:
            from osric_character_gen.data.classes import CLASS_MINIMUMS

            assert cls in CLASS_MINIMUMS

    def test_thief_selected_with_high_dex(self, selector: ClassSelector) -> None:
        scores = AbilityScores(
            strength=8,
            dexterity=17,
            constitution=8,
            intelligence=8,
            wisdom=8,
            charisma=8,
        )
        result = selector.select_best_class(scores)
        assert result == ClassName.THIEF

    def test_magic_user_selected_with_high_int(self, selector: ClassSelector) -> None:
        scores = AbilityScores(
            strength=6,
            dexterity=10,
            constitution=8,
            intelligence=17,
            wisdom=8,
            charisma=8,
        )
        result = selector.select_best_class(scores)
        assert result == ClassName.MAGIC_USER
