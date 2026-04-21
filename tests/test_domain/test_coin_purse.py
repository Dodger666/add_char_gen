"""Tests for coin denomination conversion."""

import pytest

from osric_character_gen.models.character import CoinPurse


class TestCoinPurse:
    def test_zero_gold(self) -> None:
        purse = CoinPurse.from_gold(0.0)
        assert purse.platinum == 0
        assert purse.gold == 0
        assert purse.electrum == 0
        assert purse.silver == 0
        assert purse.copper == 0

    def test_exact_gold(self) -> None:
        purse = CoinPurse.from_gold(10.0)
        assert purse.platinum == 2
        assert purse.gold == 0
        assert purse.electrum == 0
        assert purse.silver == 0
        assert purse.copper == 0

    def test_gold_with_remainder(self) -> None:
        """5.5 GP = 1pp (5gp) + 1ep (0.5gp)."""
        purse = CoinPurse.from_gold(5.5)
        assert purse.platinum == 1
        assert purse.gold == 0
        assert purse.electrum == 1
        assert purse.silver == 0
        assert purse.copper == 0

    def test_small_amount(self) -> None:
        """0.13 GP = 1sp (0.1gp) + 3cp (0.03gp)."""
        purse = CoinPurse.from_gold(0.13)
        assert purse.platinum == 0
        assert purse.gold == 0
        assert purse.electrum == 0
        assert purse.silver == 1
        assert purse.copper == 3

    def test_all_denominations(self) -> None:
        """8.63 GP = 1pp + 3gp + 1ep + 1sp + 3cp."""
        purse = CoinPurse.from_gold(8.63)
        assert purse.platinum == 1
        assert purse.gold == 3
        assert purse.electrum == 1
        assert purse.silver == 1
        assert purse.copper == 3

    def test_total_in_gold(self) -> None:
        purse = CoinPurse(platinum=2, gold=3, electrum=1, silver=5, copper=10)
        expected = 2 * 5 + 3 + 0.5 + 0.5 + 0.1
        assert abs(purse.total_in_gold() - expected) < 0.01

    def test_round_trip(self) -> None:
        """Converting to coins and back should preserve value."""
        for gp in [0.0, 1.0, 5.5, 12.37, 100.99, 250.0]:
            purse = CoinPurse.from_gold(gp)
            assert abs(purse.total_in_gold() - gp) < 0.02, f"Round-trip failed for {gp}: got {purse.total_in_gold()}"

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="negative"):
            CoinPurse.from_gold(-1.0)

    def test_large_amount(self) -> None:
        """4500 GP = 900pp."""
        purse = CoinPurse.from_gold(4500.0)
        assert purse.platinum == 900
        assert purse.gold == 0
