"""Data integrity tests for all static game tables."""

import pytest

from osric_character_gen.data.ancestries import (
    ANCESTRY_ADJUSTMENTS,
    ANCESTRY_AGE_CATEGORIES,
    ANCESTRY_CLASSES,
    ANCESTRY_HEIGHT,
    ANCESTRY_LANGUAGES,
    ANCESTRY_MOVEMENT,
    ANCESTRY_SCORE_RANGES,
    ANCESTRY_STARTING_AGE,
    ANCESTRY_WEIGHT,
    STALWART_ANCESTRIES,
    STALWART_BONUS,
)
from osric_character_gen.data.armor import ARMOR_PRIORITY, ARMOR_TABLE, SHIELD_TABLE
from osric_character_gen.data.classes import (
    CLASS_ALIGNMENTS,
    CLASS_ARMOR_ALLOWED,
    CLASS_HIT_DICE_COUNT,
    CLASS_HIT_DIE,
    CLASS_MINIMUMS,
    CLASS_PRIME_REQUISITES,
    CLASS_PROFICIENCY_SLOTS,
    CLASS_SHIELD_ALLOWED,
    CLASS_SPELL_SLOTS,
    CLASS_STARTING_GOLD,
    CLASS_THAC0,
    CLASS_WEAPONS_ALLOWED,
)
from osric_character_gen.data.equipment import (
    ADVENTURING_GEAR,
    CLASS_REQUIRED_EQUIPMENT,
    GENERAL_EQUIPMENT,
)
from osric_character_gen.data.spells import (
    CLERIC_SPELLS_LEVEL_1,
    DRUID_SPELLS_LEVEL_1,
    ILLUSIONIST_SPELLS_LEVEL_1,
    MAGIC_USER_SPELLS_LEVEL_1,
)
from osric_character_gen.data.weapons import (
    AMMUNITION,
    MELEE_WEAPONS,
    MISSILE_WEAPONS,
    WEAPON_AMMO,
    WEAPON_PRIORITY,
)
from osric_character_gen.models.character import AncestryName, ClassName

ABILITIES = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]


class TestClassTables:
    """Validate all class data tables have correct structure and values."""

    def test_all_classes_have_minimums(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_MINIMUMS, f"Missing minimums for {cls}"
            for ability in ABILITIES:
                assert ability in CLASS_MINIMUMS[cls], f"Missing {ability} for {cls}"

    def test_minimum_values_in_range(self) -> None:
        for cls, mins in CLASS_MINIMUMS.items():
            for ability, val in mins.items():
                if val is not None:
                    assert 3 <= val <= 18, f"{cls} {ability} minimum {val} out of range"

    def test_all_classes_have_hit_die(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_HIT_DIE
            assert CLASS_HIT_DIE[cls] in (4, 6, 8, 10)

    def test_all_classes_have_hit_dice_count(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_HIT_DICE_COUNT
            assert CLASS_HIT_DICE_COUNT[cls] in (1, 2)

    def test_all_classes_have_starting_gold(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_STARTING_GOLD
            num_dice, die_sides, multiplier = CLASS_STARTING_GOLD[cls]
            assert num_dice >= 1
            assert die_sides >= 4
            assert multiplier >= 1

    def test_all_classes_have_alignments(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_ALIGNMENTS
            assert len(CLASS_ALIGNMENTS[cls]) >= 1

    def test_all_classes_have_proficiency_slots(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_PROFICIENCY_SLOTS
            assert 1 <= CLASS_PROFICIENCY_SLOTS[cls] <= 4

    def test_all_classes_have_thac0(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_THAC0
            thac0, bthb = CLASS_THAC0[cls]
            assert 19 <= thac0 <= 21
            assert -1 <= bthb <= 1

    def test_all_classes_have_armor_restrictions(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_ARMOR_ALLOWED
            assert cls in CLASS_SHIELD_ALLOWED

    def test_all_classes_have_weapon_restrictions(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_WEAPONS_ALLOWED

    def test_all_classes_have_prime_requisites(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_PRIME_REQUISITES

    def test_all_classes_have_spell_slots(self) -> None:
        for cls in ClassName:
            assert cls in CLASS_SPELL_SLOTS

    def test_spell_caster_classes(self) -> None:
        casters = {ClassName.CLERIC, ClassName.DRUID, ClassName.MAGIC_USER, ClassName.ILLUSIONIST}
        for cls in ClassName:
            if cls in casters:
                assert CLASS_SPELL_SLOTS[cls] is not None, f"{cls} should have spells"
            else:
                assert CLASS_SPELL_SLOTS[cls] is None, f"{cls} should not have spells"

    def test_armor_names_match_armor_table(self) -> None:
        valid_armor_names = {a[0] for a in ARMOR_TABLE}
        for cls, allowed in CLASS_ARMOR_ALLOWED.items():
            for name in allowed:
                assert name in valid_armor_names, f"{cls} allows unknown armor: {name}"

    def test_weapon_names_match_weapon_tables(self) -> None:
        all_weapon_names = {w[0] for w in MELEE_WEAPONS} | {w[0] for w in MISSILE_WEAPONS}
        for cls, allowed in CLASS_WEAPONS_ALLOWED.items():
            if allowed is not None:
                for name in allowed:
                    assert name in all_weapon_names, f"{cls} allows unknown weapon: {name}"


class TestAncestryTables:
    """Validate all ancestry data tables have correct structure and values."""

    def test_all_ancestries_have_score_ranges(self) -> None:
        for anc in AncestryName:
            assert anc in ANCESTRY_SCORE_RANGES
            for ability in ABILITIES:
                assert ability in ANCESTRY_SCORE_RANGES[anc]
                lo, hi = ANCESTRY_SCORE_RANGES[anc][ability]
                assert 3 <= lo <= hi <= 19

    def test_all_ancestries_have_adjustments(self) -> None:
        for anc in AncestryName:
            assert anc in ANCESTRY_ADJUSTMENTS

    def test_all_ancestries_have_classes(self) -> None:
        for anc in AncestryName:
            assert anc in ANCESTRY_CLASSES
            assert len(ANCESTRY_CLASSES[anc]) >= 1

    def test_human_has_all_classes(self) -> None:
        for cls in ClassName:
            assert cls in ANCESTRY_CLASSES[AncestryName.HUMAN]

    def test_all_ancestries_have_height_weight(self) -> None:
        for anc in AncestryName:
            assert anc in ANCESTRY_HEIGHT
            base, num_d, die_sides = ANCESTRY_HEIGHT[anc]
            assert base >= 30
            assert num_d >= 1
            assert die_sides >= 2

            assert anc in ANCESTRY_WEIGHT

    def test_all_ancestries_have_starting_age(self) -> None:
        for anc in AncestryName:
            assert anc in ANCESTRY_STARTING_AGE
            for cls in ANCESTRY_CLASSES[anc]:
                assert cls in ANCESTRY_STARTING_AGE[anc], f"Missing age for {anc}/{cls}"

    def test_all_ancestries_have_age_categories(self) -> None:
        for anc in AncestryName:
            assert anc in ANCESTRY_AGE_CATEGORIES

    def test_all_ancestries_have_movement(self) -> None:
        for anc in AncestryName:
            assert anc in ANCESTRY_MOVEMENT
            assert ANCESTRY_MOVEMENT[anc] in (90, 120)

    def test_all_ancestries_have_languages(self) -> None:
        for anc in AncestryName:
            assert anc in ANCESTRY_LANGUAGES
            assert len(ANCESTRY_LANGUAGES[anc]) >= 1

    def test_stalwart_ancestries_subset(self) -> None:
        assert {
            AncestryName.DWARF,
            AncestryName.GNOME,
            AncestryName.HALFLING,
        } == STALWART_ANCESTRIES

    def test_stalwart_bonus_values(self) -> None:
        for con, bonus in STALWART_BONUS.items():
            assert isinstance(con, int)
            assert isinstance(bonus, int)
            assert bonus >= 1

    def test_ancestry_class_consistency(self) -> None:
        """Classes in ANCESTRY_CLASSES must exist in ClassName enum."""
        for anc, classes in ANCESTRY_CLASSES.items():
            for cls in classes:
                assert isinstance(cls, ClassName), f"{anc} has invalid class: {cls}"


class TestArmorTables:
    """Validate armor data integrity."""

    def test_armor_table_structure(self) -> None:
        assert len(ARMOR_TABLE) == 9
        for name, ac_desc, ac_asc, weight, move_cap, cost in ARMOR_TABLE:
            assert isinstance(name, str)
            assert 3 <= ac_desc <= 8, f"{name} AC desc {ac_desc} out of range"
            assert 12 <= ac_asc <= 17, f"{name} AC asc {ac_asc} out of range"
            assert ac_desc + ac_asc == 20, f"{name} AC desc+asc != 20"
            assert weight > 0
            assert move_cap in (60, 90, 120)
            assert cost > 0

    def test_shield_table_structure(self) -> None:
        assert len(SHIELD_TABLE) == 3
        for name, weight, cost in SHIELD_TABLE:
            assert isinstance(name, str)
            assert weight > 0
            assert cost > 0

    def test_armor_priority_names_valid(self) -> None:
        valid_names = {a[0] for a in ARMOR_TABLE}
        for category, names in ARMOR_PRIORITY.items():
            for name in names:
                assert name in valid_names, f"Priority '{category}' has unknown: {name}"


class TestWeaponTables:
    """Validate weapon data integrity."""

    def test_melee_weapons_structure(self) -> None:
        assert len(MELEE_WEAPONS) >= 20
        seen_names: set[str] = set()
        for name, hands, dmg_sm, dmg_l, weight, cost in MELEE_WEAPONS:
            assert name not in seen_names, f"Duplicate melee weapon: {name}"
            seen_names.add(name)
            assert hands in (1, 2)
            assert isinstance(dmg_sm, str)
            assert isinstance(dmg_l, str)
            assert weight > 0
            assert cost >= 0

    def test_missile_weapons_structure(self) -> None:
        assert len(MISSILE_WEAPONS) >= 5
        for _name, hands, _dmg_sm, _dmg_l, range_ft, _rof, weight, cost in MISSILE_WEAPONS:
            assert hands in (1, 2)
            assert range_ft > 0
            assert weight > 0
            assert cost >= 0

    def test_ammo_for_missile_weapons(self) -> None:
        for weapon, ammo in WEAPON_AMMO.items():
            ammo_names = {a[0] for a in AMMUNITION}
            assert ammo in ammo_names, f"Weapon '{weapon}' needs unknown ammo: {ammo}"

    def test_weapon_priority_names_valid(self) -> None:
        all_weapon_names = {w[0] for w in MELEE_WEAPONS} | {w[0] for w in MISSILE_WEAPONS}
        for cls, weapons in WEAPON_PRIORITY.items():
            for name in weapons:
                assert name in all_weapon_names, f"Priority for {cls} has unknown: {name}"


class TestSpellTables:
    """Validate spell list integrity."""

    def test_cleric_spells_count(self) -> None:
        assert len(CLERIC_SPELLS_LEVEL_1) == 12

    def test_druid_spells_count(self) -> None:
        assert len(DRUID_SPELLS_LEVEL_1) == 11

    def test_magic_user_spells_count(self) -> None:
        assert len(MAGIC_USER_SPELLS_LEVEL_1) == 30

    def test_illusionist_spells_count(self) -> None:
        assert len(ILLUSIONIST_SPELLS_LEVEL_1) == 12

    def test_read_magic_in_magic_user_list(self) -> None:
        assert "Read Magic" in MAGIC_USER_SPELLS_LEVEL_1

    def test_cure_light_wounds_in_cleric_list(self) -> None:
        assert "Cure Light Wounds" in CLERIC_SPELLS_LEVEL_1

    def test_no_duplicate_spells(self) -> None:
        for name, spells in [
            ("Cleric", CLERIC_SPELLS_LEVEL_1),
            ("Druid", DRUID_SPELLS_LEVEL_1),
            ("Magic-User", MAGIC_USER_SPELLS_LEVEL_1),
            ("Illusionist", ILLUSIONIST_SPELLS_LEVEL_1),
        ]:
            assert len(spells) == len(set(spells)), f"Duplicate spells in {name} list"

    def test_all_spells_non_empty_strings(self) -> None:
        all_spells = (
            CLERIC_SPELLS_LEVEL_1 + DRUID_SPELLS_LEVEL_1 + MAGIC_USER_SPELLS_LEVEL_1 + ILLUSIONIST_SPELLS_LEVEL_1
        )
        for spell in all_spells:
            assert isinstance(spell, str) and len(spell) > 0


class TestEquipmentTables:
    """Validate equipment data integrity."""

    def test_general_equipment_structure(self) -> None:
        assert len(GENERAL_EQUIPMENT) >= 5
        for name, weight, cost in GENERAL_EQUIPMENT:
            assert isinstance(name, str) and len(name) > 0
            assert weight >= 0
            assert cost >= 0

    def test_class_required_equipment_valid_classes(self) -> None:
        valid_names = {cls.value for cls in ClassName}
        for cls in CLASS_REQUIRED_EQUIPMENT:
            assert cls in valid_names, f"Invalid class in required equipment: {cls}"

    def test_adventuring_gear_non_empty(self) -> None:
        assert len(ADVENTURING_GEAR) >= 1


class TestCrossTableConsistency:
    """Cross-table validation tests."""

    @pytest.mark.parametrize("ancestry", list(AncestryName))
    def test_ancestry_classes_exist_in_class_tables(self, ancestry: AncestryName) -> None:
        for cls in ANCESTRY_CLASSES[ancestry]:
            assert cls in CLASS_MINIMUMS, f"{ancestry}/{cls} not in CLASS_MINIMUMS"
            assert cls in CLASS_HIT_DIE, f"{ancestry}/{cls} not in CLASS_HIT_DIE"

    def test_score_ranges_consistent_with_adjustments(self) -> None:
        """Adjusted min should not exceed adjusted max for any ancestry/ability."""
        for anc in AncestryName:
            adjustments = ANCESTRY_ADJUSTMENTS[anc]
            ranges = ANCESTRY_SCORE_RANGES[anc]
            for ability in ABILITIES:
                adj = adjustments.get(ability, 0)
                lo, hi = ranges[ability]
                # Adjusted range [lo, hi] must be valid
                assert lo <= hi, f"{anc} {ability}: min {lo} > max {hi}"
                # With positive adjustment, max should exceed base 18
                if adj > 0:
                    assert hi >= 18, f"{anc} {ability}: max {hi} too low for +{adj}"
