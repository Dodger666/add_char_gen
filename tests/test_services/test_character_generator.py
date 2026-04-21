"""Tests for CharacterGeneratorService."""

import pytest

from osric_character_gen.models.character import ClassName
from osric_character_gen.services.character_generator import (
    CharacterGeneratorService,
)


@pytest.fixture
def service() -> CharacterGeneratorService:
    return CharacterGeneratorService()


class TestCharacterGeneratorService:
    def test_generate_returns_valid_character(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        sheet, meta = service.generate(seed=42)
        assert sheet.level == 1
        assert sheet.hit_points >= 1
        assert sheet.character_class in ClassName
        assert sheet.generation_seed == 42

    def test_deterministic_generation(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        sheet1, _ = service.generate(seed=123)
        sheet2, _ = service.generate(seed=123)
        assert sheet1.character_class == sheet2.character_class
        assert sheet1.ancestry == sheet2.ancestry
        assert sheet1.ability_scores == sheet2.ability_scores
        assert sheet1.hit_points == sheet2.hit_points

    def test_different_seeds_different_characters(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        sheet1, _ = service.generate(seed=1)
        sheet2, _ = service.generate(seed=2)
        # Very unlikely to be identical
        assert sheet1.character_class != sheet2.character_class or sheet1.ability_scores != sheet2.ability_scores

    def test_metadata_contains_info(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        _, meta = service.generate(seed=42)
        assert "retries" in meta
        assert "eligible_classes" in meta
        assert "seed" in meta

    def test_generate_without_seed(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        sheet, meta = service.generate()
        assert sheet.generation_seed is not None
        assert sheet.hit_points >= 1

    def test_ability_scores_in_valid_range(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        sheet, _ = service.generate(seed=42)
        scores = sheet.ability_scores
        for attr in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            val = getattr(scores, attr)
            assert 1 <= val <= 19, f"{attr}={val} out of range"

    def test_armor_class_consistency(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        sheet, _ = service.generate(seed=42)
        assert sheet.armor_class_desc + sheet.armor_class_asc == 20

    def test_gold_remaining_non_negative(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        for seed in range(10):
            sheet, _ = service.generate(seed=seed)
            assert sheet.gold_remaining >= 0

    def test_weapons_purchased(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        sheet, _ = service.generate(seed=42)
        # Should have at least one weapon (even a staff)
        assert len(sheet.weapons) >= 1

    def test_cleric_has_turn_undead(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        # Find a seed that produces a cleric
        for seed in range(200):
            sheet, _ = service.generate(seed=seed)
            if sheet.character_class == ClassName.CLERIC:
                assert sheet.turn_undead is not None
                assert len(sheet.turn_undead) > 0
                return
        pytest.skip("No cleric generated in seed range 0-199")

    def test_thief_has_skills(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        for seed in range(200):
            sheet, _ = service.generate(seed=seed)
            if sheet.character_class == ClassName.THIEF:
                assert sheet.thief_skills is not None
                return
        pytest.skip("No thief generated in seed range 0-199")

    def test_multiple_generations_no_crash(
        self,
        service: CharacterGeneratorService,
    ) -> None:
        """Generate 50 characters to check for crashes."""
        for seed in range(50):
            sheet, meta = service.generate(seed=seed)
            assert sheet.hit_points >= 1


class TestExceptionalStrength:
    """Fighter types with 18 STR must always have exceptional strength."""

    def test_fighter_18_str_has_exceptional(self, service: CharacterGeneratorService) -> None:
        """Any fighter-type with final STR 18 must have exceptional strength, even if age brought it to 18."""
        fighter_types = {ClassName.FIGHTER, ClassName.PALADIN, ClassName.RANGER}
        found = False
        for seed in range(2000):
            sheet, _ = service.generate(seed=seed)
            if sheet.character_class in fighter_types and sheet.ability_scores.strength == 18:
                assert sheet.ability_scores.exceptional_strength is not None, (
                    f"seed={seed}: {sheet.character_class.value} has STR 18 but no exceptional strength"
                )
                found = True
        assert found, "No fighter-type with STR 18 found in 2000 seeds — test is vacuous"

    def test_seed_14_fighter_has_exceptional(self, service: CharacterGeneratorService) -> None:
        """Regression: seed 14 produces a Dwarf Fighter whose age bumps STR to 18."""
        sheet, _ = service.generate(seed=14)
        if sheet.character_class == ClassName.FIGHTER and sheet.ability_scores.strength == 18:
            assert sheet.ability_scores.exceptional_strength is not None


class TestLevelChoice:
    """Tests for multi-level character generation."""

    def test_level_parameter_sets_level(self, service: CharacterGeneratorService) -> None:
        sheet, _ = service.generate(seed=42, level=5)
        assert sheet.level == 5

    def test_level_1_default(self, service: CharacterGeneratorService) -> None:
        sheet, _ = service.generate(seed=42)
        assert sheet.level == 1

    def test_level_5_more_hp_than_level_1(self, service: CharacterGeneratorService) -> None:
        sheet1, _ = service.generate(seed=42, level=1)
        sheet5, _ = service.generate(seed=42, level=5)
        assert sheet5.hit_points > sheet1.hit_points

    def test_level_5_better_thac0(self, service: CharacterGeneratorService) -> None:
        """Higher level should have equal or lower THAC0 (better)."""
        sheet1, _ = service.generate(seed=42, level=1)
        sheet5, _ = service.generate(seed=42, level=5)
        assert sheet5.thac0 <= sheet1.thac0

    def test_level_5_has_xp(self, service: CharacterGeneratorService) -> None:
        sheet, _ = service.generate(seed=42, level=5)
        assert sheet.xp > 0

    def test_level_deterministic(self, service: CharacterGeneratorService) -> None:
        s1, _ = service.generate(seed=42, level=7)
        s2, _ = service.generate(seed=42, level=7)
        assert s1.hit_points == s2.hit_points
        assert s1.thac0 == s2.thac0
        assert s1.saving_throws == s2.saving_throws

    def test_level_10_multiple_seeds(self, service: CharacterGeneratorService) -> None:
        """Generate 10 level-10 characters without crash."""
        for seed in range(10):
            sheet, _ = service.generate(seed=seed, level=10)
            assert sheet.level == 10
            assert sheet.hit_points >= 1

    def test_caster_level_5_has_higher_spell_slots(self, service: CharacterGeneratorService) -> None:
        """Find a caster and verify higher level gets more spell slots."""
        casters = {ClassName.CLERIC, ClassName.MAGIC_USER, ClassName.DRUID, ClassName.ILLUSIONIST}
        for seed in range(200):
            sheet1, _ = service.generate(seed=seed, level=1)
            if sheet1.character_class in casters:
                sheet5, _ = service.generate(seed=seed, level=5)
                assert sheet5.spell_slots is not None
                total1 = sum(getattr(sheet1.spell_slots, f"level_{i}") for i in range(1, 8))
                total5 = sum(getattr(sheet5.spell_slots, f"level_{i}") for i in range(1, 8))
                assert total5 > total1
                return
        pytest.skip("No caster found in seed range")

    def test_thief_level_10_higher_skills(self, service: CharacterGeneratorService) -> None:
        """Higher level thief should have better skills."""
        for seed in range(200):
            sheet1, _ = service.generate(seed=seed, level=1)
            if sheet1.character_class == ClassName.THIEF:
                sheet10, _ = service.generate(seed=seed, level=10)
                assert sheet10.thief_skills.pick_locks > sheet1.thief_skills.pick_locks
                return
        pytest.skip("No thief found in seed range")

    def test_cleric_level_9_more_turn_undead(self, service: CharacterGeneratorService) -> None:
        """Higher level cleric can turn more types."""
        for seed in range(200):
            sheet1, _ = service.generate(seed=seed, level=1)
            if sheet1.character_class == ClassName.CLERIC:
                sheet9, _ = service.generate(seed=seed, level=9)
                assert len(sheet9.turn_undead) > len(sheet1.turn_undead)
                return
        pytest.skip("No cleric found in seed range")

    def test_level_capped_at_class_max(self, service: CharacterGeneratorService) -> None:
        """Requesting level above class max should cap at class max."""
        # Monk max is 17, Druid max is 14
        from osric_character_gen.data.classes import CLASS_MAX_LEVEL

        for seed in range(200):
            sheet, _ = service.generate(seed=seed, level=20)
            max_lvl = CLASS_MAX_LEVEL[sheet.character_class]
            assert sheet.level <= max_lvl
