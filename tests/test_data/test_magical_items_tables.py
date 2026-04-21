"""Tests for magical items data table integrity."""

from osric_character_gen.data.magical_items import (
    ARMOR_BASE_AC,
    BRACERS_AC,
    EXCLUSIVE_ARMOR_PRIORITY,
    EXCLUSIVE_WEAPON_PRIORITY,
    MISCELLANEOUS_ITEMS,
    POTION_AUTO_SELECT_PRIORITY,
    POTION_TYPES,
    POTIONS_TABLE,
    PROTECTION_SCROLL_TYPES,
    PROTECTIVE_ITEMS_TABLE,
    SCROLLS_TABLE,
    WEAPON_DISPLAY_NAMES,
    WEAPONS_TABLE,
    get_misc_item_count,
)
from osric_character_gen.models.character import ClassName


class TestProtectiveItemsTable:
    def test_all_classes_have_entries(self) -> None:
        for cls in ClassName:
            assert cls in PROTECTIVE_ITEMS_TABLE, f"Missing {cls}"

    def test_percentages_are_valid(self) -> None:
        for cls, items in PROTECTIVE_ITEMS_TABLE.items():
            for key, value in items.items():
                if key == "exclusive_armor":
                    assert isinstance(value, dict)
                    for armor_type, pct in value.items():
                        assert 0 < pct <= 20, f"{cls} {armor_type} pct={pct}"
                else:
                    assert 0 < value <= 20, f"{cls} {key} pct={value}"

    def test_exclusive_armor_types_in_base_ac(self) -> None:
        for armor_type in EXCLUSIVE_ARMOR_PRIORITY:
            assert armor_type in ARMOR_BASE_AC

    def test_monk_has_no_items(self) -> None:
        assert PROTECTIVE_ITEMS_TABLE[ClassName.MONK] == {}


class TestWeaponsTable:
    def test_all_classes_have_entries(self) -> None:
        for cls in ClassName:
            assert cls in WEAPONS_TABLE, f"Missing {cls}"

    def test_percentages_are_valid(self) -> None:
        for cls, items in WEAPONS_TABLE.items():
            for key, value in items.items():
                if key == "exclusive_weapon":
                    assert isinstance(value, dict)
                    for wpn_type, pct in value.items():
                        assert 0 < pct <= 20, f"{cls} {wpn_type} pct={pct}"
                else:
                    assert 0 < value <= 20, f"{cls} {key} pct={value}"

    def test_exclusive_weapon_priority_keys_exist(self) -> None:
        for wpn in EXCLUSIVE_WEAPON_PRIORITY:
            assert wpn in WEAPON_DISPLAY_NAMES


class TestPotionsTable:
    def test_all_classes_have_entries(self) -> None:
        for cls in ClassName:
            assert cls in POTIONS_TABLE, f"Missing {cls}"

    def test_potion_types_count(self) -> None:
        assert len(POTION_TYPES) == 10

    def test_max_potions_non_negative(self) -> None:
        for cls, (pct, max_p) in POTIONS_TABLE.items():
            assert max_p >= 0, f"{cls} max_potions={max_p}"
            assert pct >= 0, f"{cls} pct={pct}"

    def test_auto_select_potions_exist_in_types(self) -> None:
        for potion in POTION_AUTO_SELECT_PRIORITY:
            assert potion in POTION_TYPES


class TestScrollsTable:
    def test_all_classes_have_entries(self) -> None:
        for cls in ClassName:
            assert cls in SCROLLS_TABLE, f"Missing {cls}"

    def test_protection_scroll_types(self) -> None:
        assert len(PROTECTION_SCROLL_TYPES) == 6

    def test_spell_ranges_valid(self) -> None:
        for _cls, entry in SCROLLS_TABLE.items():
            for key in ("one_spell_range", "three_spell_range"):
                rng = entry[key]
                if rng is not None:
                    assert rng[0] >= 1
                    assert rng[1] >= rng[0]
                    assert rng[1] <= 7


class TestMiscellaneousItems:
    def test_item_count(self) -> None:
        assert len(MISCELLANEOUS_ITEMS) == 16

    def test_level_brackets_cover_6_to_20(self) -> None:
        for lvl in range(6, 21):
            count = get_misc_item_count(lvl)
            assert 1 <= count <= 4, f"level {lvl} count={count}"

    def test_below_level_6_returns_zero(self) -> None:
        for lvl in range(1, 6):
            assert get_misc_item_count(lvl) == 0

    def test_counts_scale_with_level(self) -> None:
        assert get_misc_item_count(6) == 1
        assert get_misc_item_count(9) == 2
        assert get_misc_item_count(13) == 3
        assert get_misc_item_count(17) == 4


class TestBracersAC:
    def test_all_bonus_levels(self) -> None:
        assert BRACERS_AC[1] == (6, 14)
        assert BRACERS_AC[2] == (5, 15)
        assert BRACERS_AC[3] == (4, 16)
