"""Tests for MagicalItemGenerator (DMG Appendix P)."""

import pytest

from osric_character_gen.domain.dice import DiceRoller
from osric_character_gen.domain.magical_item_generator import MagicalItemGenerator
from osric_character_gen.models.character import AncestryName, ClassName, MagicalItem


@pytest.fixture
def roller() -> DiceRoller:
    return DiceRoller(seed=42)


@pytest.fixture
def gen(roller: DiceRoller) -> MagicalItemGenerator:
    return MagicalItemGenerator(roller)


class TestLevelGating:
    def test_level_1_no_items(self, gen: MagicalItemGenerator) -> None:
        items = gen.generate_magical_items(ClassName.FIGHTER, 1, AncestryName.HUMAN)
        assert items == []

    def test_level_2_can_have_items(self) -> None:
        """Over many seeds, at least one level-2 character gets something."""
        found = False
        for seed in range(200):
            roller = DiceRoller(seed=seed)
            g = MagicalItemGenerator(roller)
            items = g.generate_magical_items(ClassName.FIGHTER, 2, AncestryName.HUMAN)
            if items:
                found = True
                break
        assert found, "No items found for level 2 fighter across 200 seeds"


class TestDeterminism:
    def test_same_seed_same_items(self) -> None:
        r1 = DiceRoller(seed=99)
        r2 = DiceRoller(seed=99)
        g1 = MagicalItemGenerator(r1)
        g2 = MagicalItemGenerator(r2)
        items1 = g1.generate_magical_items(ClassName.FIGHTER, 10, AncestryName.HUMAN)
        items2 = g2.generate_magical_items(ClassName.FIGHTER, 10, AncestryName.HUMAN)
        assert len(items1) == len(items2)
        for a, b in zip(items1, items2, strict=True):
            assert a.name == b.name
            assert a.bonus == b.bonus


class TestProtectiveItems:
    def test_fighter_can_get_magic_armor(self) -> None:
        """High-level fighter should often get armor across many seeds."""
        got_armor = False
        for seed in range(200):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 10, AncestryName.HUMAN)
            armor = [i for i in items if i.item_type == "armor"]
            if armor:
                got_armor = True
                assert armor[0].bonus >= 1
                break
        assert got_armor

    def test_mu_gets_ring_or_bracers(self) -> None:
        """MU at level 10 often gets ring of protection or bracers."""
        got = False
        for seed in range(200):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.MAGIC_USER, 10, AncestryName.HUMAN)
            rings_or_bracers = [i for i in items if i.item_type in ("ring", "bracers")]
            if rings_or_bracers:
                got = True
                break
        assert got

    def test_thief_no_heavy_armor(self) -> None:
        """Thief never gets plate, chain, or banded."""
        heavy = {"Plate Mail", "Chain Mail", "Banded Mail"}
        for seed in range(200):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.THIEF, 10, AncestryName.HUMAN)
            for item in items:
                assert item.name.split(" +")[0] not in heavy

    def test_monk_no_protective_items(self) -> None:
        for seed in range(50):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.MONK, 10, AncestryName.HUMAN)
            prot = [i for i in items if i.item_type in ("armor", "shield", "ring", "bracers")]
            assert prot == []


class TestEnhancement:
    def test_high_level_can_get_plus_2(self) -> None:
        """At level 15, across many seeds, some item should be +2."""
        found_plus_2 = False
        for seed in range(500):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 15, AncestryName.HUMAN)
            for item in items:
                if item.bonus and item.bonus >= 2:
                    found_plus_2 = True
                    break
            if found_plus_2:
                break
        assert found_plus_2

    def test_enhancement_never_exceeds_3(self) -> None:
        for seed in range(200):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 20, AncestryName.HUMAN)
            for item in items:
                if item.bonus is not None:
                    assert item.bonus <= 3


class TestWeapons:
    def test_fighter_can_get_magic_weapon(self) -> None:
        got_weapon = False
        for seed in range(200):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 10, AncestryName.HUMAN)
            weapons = [i for i in items if i.item_type == "weapon"]
            if weapons:
                got_weapon = True
                break
        assert got_weapon

    def test_druid_sword_is_scimitar(self) -> None:
        """Druid's 'sword' entry should produce a Scimitar."""
        for seed in range(500):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.DRUID, 10, AncestryName.HUMAN)
            swords = [i for i in items if "Sword" in i.name or "Scimitar" in i.name]
            for s in swords:
                assert "Scimitar" in s.name, f"Expected Scimitar, got {s.name}"

    def test_small_ancestry_short_sword(self) -> None:
        """Halfling gets Short Sword instead of Long Sword."""
        for seed in range(500):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.THIEF, 10, AncestryName.HALFLING)
            swords = [i for i in items if "Sword" in i.name]
            for s in swords:
                assert "Short Sword" in s.name, f"Expected Short Sword, got {s.name}"


class TestPotions:
    def test_potion_max_respected(self) -> None:
        """Fighter max potions = 1."""
        for seed in range(200):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 15, AncestryName.HUMAN)
            potions = [i for i in items if i.item_type == "potion"]
            assert len(potions) <= 1

    def test_mu_can_get_multiple_potions(self) -> None:
        """MU max potions = 3, at high level should get multiple sometimes."""
        got_multiple = False
        for seed in range(500):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.MAGIC_USER, 15, AncestryName.HUMAN)
            potions = [i for i in items if i.item_type == "potion"]
            if len(potions) >= 2:
                got_multiple = True
                break
        assert got_multiple

    def test_monk_no_potions(self) -> None:
        for seed in range(50):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.MONK, 10, AncestryName.HUMAN)
            potions = [i for i in items if i.item_type == "potion"]
            assert potions == []

    def test_potion_name_is_valid(self) -> None:
        from osric_character_gen.data.magical_items import POTION_TYPES

        for seed in range(200):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.THIEF, 10, AncestryName.HUMAN)
            for item in items:
                if item.item_type == "potion":
                    potion_name = item.name.replace("Potion of ", "")
                    assert potion_name in POTION_TYPES, f"Unknown potion: {item.name}"


class TestScrolls:
    def test_caster_can_get_spell_scroll(self) -> None:
        got_spell = False
        for seed in range(500):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.MAGIC_USER, 10, AncestryName.HUMAN)
            scrolls = [i for i in items if i.item_type == "scroll"]
            for s in scrolls:
                if s.properties.get("spells"):
                    got_spell = True
                    break
            if got_spell:
                break
        assert got_spell

    def test_fighter_gets_protection_scroll(self) -> None:
        """Fighter can only get protection scrolls."""
        for seed in range(500):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 10, AncestryName.HUMAN)
            scrolls = [i for i in items if i.item_type == "scroll"]
            for s in scrolls:
                assert "Protection" in s.name, f"Fighter got non-protection scroll: {s.name}"

    def test_monk_no_scrolls(self) -> None:
        for seed in range(50):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.MONK, 10, AncestryName.HUMAN)
            scrolls = [i for i in items if i.item_type == "scroll"]
            assert scrolls == []


class TestMiscellaneous:
    def test_no_misc_below_level_6(self) -> None:
        for seed in range(100):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 5, AncestryName.HUMAN)
            misc = [i for i in items if i.item_type == "miscellaneous"]
            assert misc == []

    def test_level_6_gets_miscellaneous(self) -> None:
        """Level 6 should get exactly 1 misc item."""
        r = DiceRoller(seed=42)
        g = MagicalItemGenerator(r)
        items = g.generate_magical_items(ClassName.FIGHTER, 6, AncestryName.HUMAN)
        misc = [i for i in items if i.item_type == "miscellaneous"]
        assert len(misc) == 1

    def test_level_10_gets_two_misc(self) -> None:
        r = DiceRoller(seed=42)
        g = MagicalItemGenerator(r)
        items = g.generate_magical_items(ClassName.FIGHTER, 10, AncestryName.HUMAN)
        misc = [i for i in items if i.item_type == "miscellaneous"]
        assert len(misc) == 2

    def test_no_duplicate_misc_items(self) -> None:
        for seed in range(100):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 20, AncestryName.HUMAN)
            misc = [i for i in items if i.item_type == "miscellaneous"]
            names = [m.name for m in misc]
            assert len(names) == len(set(names)), f"Duplicates found: {names}"

    def test_misc_items_are_from_table(self) -> None:
        from osric_character_gen.data.magical_items import MISCELLANEOUS_ITEMS

        for seed in range(100):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 10, AncestryName.HUMAN)
            for item in items:
                if item.item_type == "miscellaneous":
                    assert item.name in MISCELLANEOUS_ITEMS, f"Unknown misc: {item.name}"


class TestReturnTypes:
    def test_returns_list_of_magical_item(self, gen: MagicalItemGenerator) -> None:
        items = gen.generate_magical_items(ClassName.FIGHTER, 10, AncestryName.HUMAN)
        assert isinstance(items, list)
        for item in items:
            assert isinstance(item, MagicalItem)

    def test_item_types_are_valid(self) -> None:
        valid_types = {
            "armor",
            "shield",
            "weapon",
            "potion",
            "scroll",
            "ring",
            "bracers",
            "miscellaneous",
            "ammunition",
        }
        for seed in range(100):
            r = DiceRoller(seed=seed)
            g = MagicalItemGenerator(r)
            items = g.generate_magical_items(ClassName.FIGHTER, 15, AncestryName.HUMAN)
            for item in items:
                assert item.item_type in valid_types, f"Invalid type: {item.item_type}"
