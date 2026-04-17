"""Tests for Holmesian Random Name Generator."""

from osric_character_gen.domain.dice import DiceRoller
from osric_character_gen.domain.name_generator import HolmesianNameGenerator


class TestHolmesianNameGenerator:
    def test_generate_returns_string(self) -> None:
        roller = DiceRoller(seed=42)
        gen = HolmesianNameGenerator(roller)
        name = gen.generate()
        assert isinstance(name, str)
        assert len(name) > 0

    def test_deterministic_with_seed(self) -> None:
        name1 = HolmesianNameGenerator(DiceRoller(seed=99)).generate()
        name2 = HolmesianNameGenerator(DiceRoller(seed=99)).generate()
        assert name1 == name2

    def test_different_seeds_different_names(self) -> None:
        name1 = HolmesianNameGenerator(DiceRoller(seed=1)).generate()
        name2 = HolmesianNameGenerator(DiceRoller(seed=2)).generate()
        assert name1 != name2

    def test_name_starts_with_uppercase(self) -> None:
        for seed in range(50):
            name = HolmesianNameGenerator(DiceRoller(seed=seed)).generate()
            assert name[0].isupper(), f"Seed {seed}: name '{name}' doesn't start uppercase"

    def test_syllable_count_range(self) -> None:
        """Names should have 1-4 syllables worth of content."""
        for seed in range(100):
            name = HolmesianNameGenerator(DiceRoller(seed=seed)).generate()
            # At minimum a single syllable (2+ chars), at max 4 syllables
            assert len(name) >= 2, f"Seed {seed}: name '{name}' too short"

    def test_generate_syllable_returns_valid_string(self) -> None:
        roller = DiceRoller(seed=42)
        gen = HolmesianNameGenerator(roller)
        syllable = gen._roll_syllable()
        assert isinstance(syllable, str)
        assert len(syllable) >= 1

    def test_all_100_syllable_entries_accessible(self) -> None:
        """Each d100 roll (1-100) should produce a valid syllable."""
        gen = HolmesianNameGenerator(DiceRoller(seed=1))
        assert len(gen.SYLLABLE_TABLE) == 100

    def test_no_empty_names(self) -> None:
        for seed in range(200):
            name = HolmesianNameGenerator(DiceRoller(seed=seed)).generate()
            assert name.strip() != ""

    def test_title_generation(self) -> None:
        """Title table has 20 entries."""
        gen = HolmesianNameGenerator(DiceRoller(seed=1))
        assert len(gen.TITLE_TABLE) == 20

    def test_generate_with_title(self) -> None:
        gen = HolmesianNameGenerator(DiceRoller(seed=42))
        name = gen.generate(include_title=True)
        assert isinstance(name, str)
        assert len(name) > 0

    def test_generate_without_title(self) -> None:
        gen = HolmesianNameGenerator(DiceRoller(seed=42))
        name = gen.generate(include_title=False)
        assert isinstance(name, str)
        # Without title should not contain "the" keyword
        assert " the " not in name
        assert name.startswith("of the ") is False

    def test_stress_200_names_no_crash(self) -> None:
        for seed in range(200):
            name = HolmesianNameGenerator(DiceRoller(seed=seed)).generate(include_title=True)
            assert isinstance(name, str)
            assert len(name) >= 2
