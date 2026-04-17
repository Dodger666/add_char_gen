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
