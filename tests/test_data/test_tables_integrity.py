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


class TestSavingThrowProgression:
    """Validate full saving throw progression tables."""

    def test_all_classes_have_save_tables(self) -> None:
        from osric_character_gen.data.saving_throws import SAVING_THROW_TABLES

        for cls in ClassName:
            assert cls in SAVING_THROW_TABLES, f"Missing save table for {cls}"

    def test_get_saving_throws_level_1_matches_legacy(self) -> None:
        from osric_character_gen.data.saving_throws import SAVING_THROWS_LEVEL_1, get_saving_throws

        for cls in ClassName:
            legacy = SAVING_THROWS_LEVEL_1[cls]
            new = get_saving_throws(cls, 1)
            assert legacy == new, f"{cls} level 1 mismatch: {legacy} vs {new}"

    def test_saves_improve_with_level(self) -> None:
        from osric_character_gen.data.saving_throws import get_saving_throws

        for cls in ClassName:
            low = get_saving_throws(cls, 1)
            high = get_saving_throws(cls, 20)
            # All saves should improve (lower numbers are better)
            for i in range(5):
                assert high[i] <= low[i], f"{cls} save index {i} did not improve from level 1 to 20"

    def test_fighter_level_5_saves(self) -> None:
        from osric_character_gen.data.saving_throws import get_saving_throws

        saves = get_saving_throws(ClassName.FIGHTER, 5)
        assert saves == (13, 13, 11, 12, 14)

    def test_paladin_level_10_saves(self) -> None:
        from osric_character_gen.data.saving_throws import get_saving_throws

        saves = get_saving_throws(ClassName.PALADIN, 10)
        assert saves == (8, 7, 6, 7, 9)


class TestThac0Progression:
    """Validate full THAC0/BTHB progression tables."""

    def test_all_classes_have_thac0_tables(self) -> None:
        from osric_character_gen.data.classes import THAC0_TABLES

        for cls in ClassName:
            assert cls in THAC0_TABLES, f"Missing THAC0 table for {cls}"

    def test_get_thac0_level_1_matches_legacy(self) -> None:
        from osric_character_gen.data.classes import CLASS_THAC0, get_thac0

        for cls in ClassName:
            legacy = CLASS_THAC0[cls]
            new = get_thac0(cls, 1)
            assert legacy == new, f"{cls} level 1 THAC0 mismatch: {legacy} vs {new}"

    def test_fighter_level_5(self) -> None:
        from osric_character_gen.data.classes import get_thac0

        assert get_thac0(ClassName.FIGHTER, 5) == (16, 4)

    def test_thief_level_9(self) -> None:
        from osric_character_gen.data.classes import get_thac0

        assert get_thac0(ClassName.THIEF, 9) == (16, 4)

    def test_magic_user_level_16(self) -> None:
        from osric_character_gen.data.classes import get_thac0

        assert get_thac0(ClassName.MAGIC_USER, 16) == (11, 9)


class TestSpellSlotProgression:
    """Validate full spell slot progression tables."""

    def test_cleric_level_1_matches(self) -> None:
        from osric_character_gen.data.classes import SPELL_SLOT_TABLES

        assert SPELL_SLOT_TABLES[ClassName.CLERIC][1] == (1, 0, 0, 0, 0, 0, 0)

    def test_cleric_level_9(self) -> None:
        from osric_character_gen.data.classes import SPELL_SLOT_TABLES

        assert SPELL_SLOT_TABLES[ClassName.CLERIC][9] == (4, 4, 3, 2, 1, 0, 0)

    def test_magic_user_level_14(self) -> None:
        from osric_character_gen.data.classes import SPELL_SLOT_TABLES

        assert SPELL_SLOT_TABLES[ClassName.MAGIC_USER][14] == (5, 5, 5, 4, 4, 2, 1)

    def test_paladin_no_spells_before_9(self) -> None:
        from osric_character_gen.data.classes import SPELL_SLOT_TABLES

        for lvl in range(1, 9):
            assert SPELL_SLOT_TABLES[ClassName.PALADIN][lvl] == (0, 0, 0, 0, 0, 0, 0)

    def test_paladin_gets_spells_at_9(self) -> None:
        from osric_character_gen.data.classes import SPELL_SLOT_TABLES

        assert SPELL_SLOT_TABLES[ClassName.PALADIN][9] == (1, 0, 0, 0, 0, 0, 0)

    def test_druid_max_level_14(self) -> None:
        from osric_character_gen.data.classes import SPELL_SLOT_TABLES

        assert 14 in SPELL_SLOT_TABLES[ClassName.DRUID]
        assert 15 not in SPELL_SLOT_TABLES[ClassName.DRUID]


class TestThiefSkillProgression:
    """Validate full thief skill progression tables."""

    def test_level_1_matches_base(self) -> None:
        from osric_character_gen.data.thief_skills import BASE_THIEF_SKILLS, THIEF_SKILLS_BY_LEVEL

        assert THIEF_SKILLS_BY_LEVEL[1] == BASE_THIEF_SKILLS

    def test_skills_increase_with_level(self) -> None:
        from osric_character_gen.data.thief_skills import THIEF_SKILLS_BY_LEVEL

        for skill in THIEF_SKILLS_BY_LEVEL[1]:
            val_1 = THIEF_SKILLS_BY_LEVEL[1][skill]
            val_17 = THIEF_SKILLS_BY_LEVEL[17][skill]
            assert val_17 >= val_1, f"{skill} did not increase from level 1 to 17"

    def test_all_levels_1_to_17_present(self) -> None:
        from osric_character_gen.data.thief_skills import THIEF_SKILLS_BY_LEVEL

        for lvl in range(1, 18):
            assert lvl in THIEF_SKILLS_BY_LEVEL


class TestTurnUndeadProgression:
    """Validate full turn undead progression tables."""

    def test_level_1_matches_legacy(self) -> None:
        from osric_character_gen.data.turn_undead import TURN_UNDEAD_LEVEL_1, get_turn_undead

        result = get_turn_undead(1)
        for i, (t, e, r) in enumerate(TURN_UNDEAD_LEVEL_1):
            if r == "—":
                continue
            assert result[i] == (t, e, r)

    def test_level_9_has_more_entries(self) -> None:
        from osric_character_gen.data.turn_undead import get_turn_undead

        t1 = get_turn_undead(1)
        t9 = get_turn_undead(9)
        assert len(t9) > len(t1)

    def test_level_9_has_destroy(self) -> None:
        from osric_character_gen.data.turn_undead import get_turn_undead

        entries = get_turn_undead(9)
        rolls = [e[2] for e in entries]
        assert "D" in rolls


class TestHigherLevelSpells:
    """Validate higher-level spell lists."""

    def test_spell_lists_all_classes_present(self) -> None:
        from osric_character_gen.data.spells import SPELL_LISTS

        for cls_name in ["Cleric", "Druid", "Magic-User", "Illusionist", "Paladin"]:
            assert cls_name in SPELL_LISTS

    def test_cleric_has_7_levels(self) -> None:
        from osric_character_gen.data.spells import SPELL_LISTS

        for lvl in range(1, 8):
            assert lvl in SPELL_LISTS["Cleric"]
            assert len(SPELL_LISTS["Cleric"][lvl]) >= 5

    def test_magic_user_has_7_levels(self) -> None:
        from osric_character_gen.data.spells import SPELL_LISTS

        for lvl in range(1, 8):
            assert lvl in SPELL_LISTS["Magic-User"]
            assert len(SPELL_LISTS["Magic-User"][lvl]) >= 5

    def test_paladin_has_4_levels_only(self) -> None:
        from osric_character_gen.data.spells import SPELL_LISTS

        assert len(SPELL_LISTS["Paladin"]) == 4

    def test_no_duplicate_spells_per_level(self) -> None:
        from osric_character_gen.data.spells import SPELL_LISTS

        for cls_name, levels in SPELL_LISTS.items():
            for lvl, spells in levels.items():
                assert len(spells) == len(set(spells)), f"Duplicates in {cls_name} level {lvl}"


class TestMonkTables:
    """Validate monk progression tables."""

    def test_monk_ac_all_levels(self) -> None:
        from osric_character_gen.data.monk_tables import MONK_AC

        for lvl in range(1, 18):
            assert lvl in MONK_AC
            desc, asc = MONK_AC[lvl]
            assert desc + asc == 20, f"Monk AC at level {lvl}: {desc}+{asc} != 20"

    def test_monk_damage_all_levels(self) -> None:
        from osric_character_gen.data.monk_tables import MONK_DAMAGE

        for lvl in range(1, 18):
            assert lvl in MONK_DAMAGE
            assert isinstance(MONK_DAMAGE[lvl], str)

    def test_monk_movement_all_levels(self) -> None:
        from osric_character_gen.data.monk_tables import MONK_MOVEMENT

        for lvl in range(1, 18):
            assert lvl in MONK_MOVEMENT
            assert MONK_MOVEMENT[lvl] >= 150

    def test_monk_movement_increases(self) -> None:
        from osric_character_gen.data.monk_tables import MONK_MOVEMENT

        assert MONK_MOVEMENT[17] > MONK_MOVEMENT[1]


class TestXPTables:
    """Validate XP progression tables."""

    def test_all_classes_have_xp_tables(self) -> None:
        from osric_character_gen.data.classes import CLASS_XP_TABLE

        for cls in ClassName:
            assert cls in CLASS_XP_TABLE

    def test_xp_starts_at_zero(self) -> None:
        from osric_character_gen.data.classes import CLASS_XP_TABLE

        for cls, table in CLASS_XP_TABLE.items():
            assert table[1] == 0, f"{cls} level 1 XP should be 0"

    def test_xp_increases_monotonically(self) -> None:
        from osric_character_gen.data.classes import CLASS_XP_TABLE

        for cls, table in CLASS_XP_TABLE.items():
            prev = -1
            for lvl in sorted(table.keys()):
                assert table[lvl] >= prev, f"{cls} XP not monotonic at level {lvl}"
                prev = table[lvl]


class TestHitDieCaps:
    """Validate hit die cap and fixed HP tables."""

    def test_all_classes_have_caps(self) -> None:
        from osric_character_gen.data.classes import CLASS_FIXED_HP_PER_LEVEL, CLASS_HIT_DIE_CAP

        for cls in ClassName:
            assert cls in CLASS_HIT_DIE_CAP
            assert cls in CLASS_FIXED_HP_PER_LEVEL

    def test_cap_within_max_level(self) -> None:
        from osric_character_gen.data.classes import CLASS_HIT_DIE_CAP, CLASS_MAX_LEVEL

        for cls in ClassName:
            assert CLASS_HIT_DIE_CAP[cls] <= CLASS_MAX_LEVEL[cls]


class TestProficiencyGainLevels:
    """Validate weapon proficiency gain schedule."""

    def test_all_classes_have_gain_levels(self) -> None:
        from osric_character_gen.data.classes import CLASS_PROFICIENCY_GAIN_LEVELS

        for cls in ClassName:
            assert cls in CLASS_PROFICIENCY_GAIN_LEVELS

    def test_gain_levels_sorted(self) -> None:
        from osric_character_gen.data.classes import CLASS_PROFICIENCY_GAIN_LEVELS

        for cls, levels in CLASS_PROFICIENCY_GAIN_LEVELS.items():
            assert levels == sorted(levels), f"{cls} gain levels not sorted"

    def test_gain_levels_above_1(self) -> None:
        from osric_character_gen.data.classes import CLASS_PROFICIENCY_GAIN_LEVELS

        for cls, levels in CLASS_PROFICIENCY_GAIN_LEVELS.items():
            for lvl in levels:
                assert lvl > 1, f"{cls} has gain level at {lvl}"
