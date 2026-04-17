"""Tests for DiceRoller."""

from osric_character_gen.domain.dice import DiceRoller


class TestDiceRoller:
    def test_roll_single_die_range(self) -> None:
        roller = DiceRoller(seed=42)
        for _ in range(100):
            result = roller.roll(6)
            assert 1 <= result <= 6

    def test_roll_multiple_returns_correct_count(self) -> None:
        roller = DiceRoller(seed=42)
        results = roller.roll_multiple(4, 6)
        assert len(results) == 4
        assert all(1 <= r <= 6 for r in results)

    def test_roll_4d6_drop_lowest_range(self) -> None:
        roller = DiceRoller(seed=42)
        for _ in range(100):
            result = roller.roll_4d6_drop_lowest()
            assert 3 <= result <= 18

    def test_roll_ability_scores_returns_six(self) -> None:
        roller = DiceRoller(seed=42)
        scores = roller.roll_ability_scores()
        assert len(scores) == 6
        assert all(3 <= s <= 18 for s in scores)

    def test_deterministic_with_seed(self) -> None:
        roller1 = DiceRoller(seed=123)
        roller2 = DiceRoller(seed=123)
        assert roller1.roll_ability_scores() == roller2.roll_ability_scores()

    def test_different_seeds_different_results(self) -> None:
        roller1 = DiceRoller(seed=1)
        roller2 = DiceRoller(seed=2)
        # Very unlikely to be the same
        scores1 = roller1.roll_ability_scores()
        scores2 = roller2.roll_ability_scores()
        assert scores1 != scores2

    def test_roll_hit_points_minimum_one(self) -> None:
        roller = DiceRoller(seed=42)
        result = roller.roll_hit_points(hit_die=4, con_mod=-10)
        assert result >= 1

    def test_roll_hit_points_multiple_dice(self) -> None:
        roller = DiceRoller(seed=42)
        result = roller.roll_hit_points(hit_die=8, con_mod=2, count=2)
        # Each die: 1-8, + 2 con each = 3-10 per die, total 6-20
        assert 4 <= result <= 20

    def test_roll_gold(self) -> None:
        roller = DiceRoller(seed=42)
        gold = roller.roll_gold(3, 6, 10)
        assert 30 <= gold <= 180

    def test_roll_gold_no_multiplier(self) -> None:
        roller = DiceRoller(seed=42)
        gold = roller.roll_gold(5, 4, 1)
        assert 5 <= gold <= 20

    def test_roll_percentile_range(self) -> None:
        roller = DiceRoller(seed=42)
        for _ in range(100):
            result = roller.roll_percentile()
            assert 1 <= result <= 100

    def test_choice(self) -> None:
        roller = DiceRoller(seed=42)
        items = ["a", "b", "c"]
        result = roller.choice(items)
        assert result in items

    def test_sample(self) -> None:
        roller = DiceRoller(seed=42)
        items = [1, 2, 3, 4, 5]
        result = roller.sample(items, 3)
        assert len(result) == 3
        assert len(set(result)) == 3
        assert all(r in items for r in result)

    def test_min_die_val(self) -> None:
        """CON 19 treats die rolls of 1 as 2."""
        roller = DiceRoller(seed=42)
        for _ in range(50):
            result = roller.roll_hit_points(hit_die=4, con_mod=0, min_die_val=2)
            assert result >= 2
