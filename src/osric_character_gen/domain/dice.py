"""Dice rolling utilities for OSRIC 3.0 character generation."""

import random


class DiceRoller:
    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self.seed = seed

    def roll(self, sides: int) -> int:
        """Roll a single die with given number of sides."""
        return self._rng.randint(1, sides)

    def roll_multiple(self, count: int, sides: int) -> list[int]:
        """Roll multiple dice, return individual results."""
        return [self.roll(sides) for _ in range(count)]

    def roll_4d6_drop_lowest(self) -> int:
        """Roll 4d6, drop lowest, return sum."""
        rolls = self.roll_multiple(4, 6)
        rolls.sort()
        return sum(rolls[1:])

    def roll_ability_scores(self) -> list[int]:
        """Roll 6 ability scores using Normal Mode."""
        return [self.roll_4d6_drop_lowest() for _ in range(6)]

    def roll_hit_points(
        self,
        hit_die: int,
        con_mod: int,
        count: int = 1,
        min_die_val: int = 1,
    ) -> int:
        """Roll hit points with CON modifier. Minimum total is 1."""
        total = 0
        for _ in range(count):
            die_roll = self.roll(hit_die)
            if die_roll < min_die_val:
                die_roll = min_die_val
            total += max(1, die_roll + con_mod)
        return max(1, total)

    def roll_hit_points_multi_level(
        self,
        hit_die: int,
        con_mod: int,
        level: int,
        hit_die_cap: int,
        fixed_hp: int,
        level_1_dice: int = 1,
        min_die_val: int = 1,
    ) -> int:
        """Roll HP for multiple levels.

        - Level 1: roll level_1_dice dice (e.g. 2 for Ranger/Monk)
        - Levels 2 through hit_die_cap: roll 1 die each
        - Levels above hit_die_cap: add fixed_hp per level (no CON bonus)
        """
        total = 0
        # Level 1
        for _ in range(level_1_dice):
            die_roll = self.roll(hit_die)
            if die_roll < min_die_val:
                die_roll = min_die_val
            total += max(1, die_roll + con_mod)
        # Levels 2 through min(level, hit_die_cap)
        for _ in range(2, min(level, hit_die_cap) + 1):
            die_roll = self.roll(hit_die)
            if die_roll < min_die_val:
                die_roll = min_die_val
            total += max(1, die_roll + con_mod)
        # Levels above hit_die_cap
        if level > hit_die_cap:
            total += fixed_hp * (level - hit_die_cap)
        return max(1, total)

    def roll_gold(self, dice_count: int, dice_sides: int, multiplier: int = 10) -> int:
        """Roll starting gold."""
        total = sum(self.roll_multiple(dice_count, dice_sides))
        return total * multiplier

    def roll_percentile(self) -> int:
        """Roll d100 (1-100)."""
        return self._rng.randint(1, 100)

    def choice(self, seq: list) -> object:
        """Choose a random element from a sequence."""
        return self._rng.choice(seq)

    def sample(self, population: list, k: int) -> list:
        """Return k unique random elements from population."""
        return self._rng.sample(population, k)

    def shuffle(self, seq: list) -> None:
        """Shuffle a list in place."""
        self._rng.shuffle(seq)
