"""Tests for PhysicalCharacteristicsGenerator."""

import pytest

from osric_character_gen.domain.dice import DiceRoller
from osric_character_gen.domain.physical_generator import (
    PhysicalCharacteristicsGenerator,
)
from osric_character_gen.models.character import AncestryName, ClassName, Gender


@pytest.fixture
def gen() -> PhysicalCharacteristicsGenerator:
    return PhysicalCharacteristicsGenerator(DiceRoller(seed=42))


class TestPhysicalGenerator:
    def test_human_height_range(self, gen: PhysicalCharacteristicsGenerator) -> None:
        physical = gen.generate(AncestryName.HUMAN, ClassName.FIGHTER)
        # Human: 64 + 3d4 = 67-76
        assert 67 <= physical.height_inches <= 76

    def test_human_weight_range(self, gen: PhysicalCharacteristicsGenerator) -> None:
        physical = gen.generate(AncestryName.HUMAN, ClassName.FIGHTER)
        # Human: 140 + 6d10 = 146-200
        assert 146 <= physical.weight_lbs <= 200

    def test_dwarf_height_range(self) -> None:
        gen = PhysicalCharacteristicsGenerator(DiceRoller(seed=99))
        physical = gen.generate(AncestryName.DWARF, ClassName.FIGHTER)
        # Dwarf: 48 + 3d4 = 51-60
        assert 51 <= physical.height_inches <= 60

    def test_height_display_format(self, gen: PhysicalCharacteristicsGenerator) -> None:
        physical = gen.generate(AncestryName.HUMAN, ClassName.FIGHTER)
        assert "'" in physical.height_display
        assert '"' in physical.height_display

    def test_gender_is_valid(self, gen: PhysicalCharacteristicsGenerator) -> None:
        physical = gen.generate(AncestryName.HUMAN, ClassName.FIGHTER)
        assert physical.gender in [Gender.MALE, Gender.FEMALE]

    def test_human_fighter_age_range(self) -> None:
        gen = PhysicalCharacteristicsGenerator(DiceRoller(seed=42))
        physical = gen.generate(AncestryName.HUMAN, ClassName.FIGHTER)
        # Human Fighter: 15 + 1d4 = 16-19
        assert 16 <= physical.age <= 19

    def test_elf_fighter_age_range(self) -> None:
        gen = PhysicalCharacteristicsGenerator(DiceRoller(seed=42))
        physical = gen.generate(AncestryName.ELF, ClassName.FIGHTER)
        # Elf Fighter: 130 + 5d6 = 135-160
        assert 135 <= physical.age <= 160

    def test_age_category_human_youth(
        self,
        gen: PhysicalCharacteristicsGenerator,
    ) -> None:
        assert gen.get_age_category(AncestryName.HUMAN, 18) == "Youth"

    def test_age_category_human_adult(
        self,
        gen: PhysicalCharacteristicsGenerator,
    ) -> None:
        assert gen.get_age_category(AncestryName.HUMAN, 25) == "Adult"

    def test_age_category_human_grizzled(
        self,
        gen: PhysicalCharacteristicsGenerator,
    ) -> None:
        assert gen.get_age_category(AncestryName.HUMAN, 45) == "Grizzled"

    def test_age_category_human_elder(
        self,
        gen: PhysicalCharacteristicsGenerator,
    ) -> None:
        assert gen.get_age_category(AncestryName.HUMAN, 65) == "Elder"

    def test_age_category_human_ancient(
        self,
        gen: PhysicalCharacteristicsGenerator,
    ) -> None:
        assert gen.get_age_category(AncestryName.HUMAN, 95) == "Ancient"

    def test_age_adjustments_adult(
        self,
        gen: PhysicalCharacteristicsGenerator,
    ) -> None:
        adj = gen.get_age_adjustments("Adult")
        assert adj.get("strength") == 1
        assert adj.get("wisdom") == 1

    def test_age_adjustments_youth(
        self,
        gen: PhysicalCharacteristicsGenerator,
    ) -> None:
        adj = gen.get_age_adjustments("Youth")
        assert adj.get("constitution") == 1
        assert adj.get("wisdom") == -1

    def test_deterministic_with_seed(self) -> None:
        gen1 = PhysicalCharacteristicsGenerator(DiceRoller(seed=42))
        gen2 = PhysicalCharacteristicsGenerator(DiceRoller(seed=42))
        p1 = gen1.generate(AncestryName.HUMAN, ClassName.FIGHTER)
        p2 = gen2.generate(AncestryName.HUMAN, ClassName.FIGHTER)
        assert p1 == p2
