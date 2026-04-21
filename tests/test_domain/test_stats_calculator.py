"""Tests for DerivedStatsCalculator."""

import pytest

from osric_character_gen.domain.stats_calculator import DerivedStatsCalculator
from osric_character_gen.models.character import (
    AbilityScores,
    AncestryName,
    ArmorItem,
    ClassName,
    EquipmentItem,
    ThiefSkills,
)


@pytest.fixture
def calc() -> DerivedStatsCalculator:
    return DerivedStatsCalculator()


class TestAbilityBonuses:
    def test_average_scores(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        bonuses = calc.calculate_ability_bonuses(scores, ClassName.FIGHTER)
        assert bonuses.str_to_hit == 0
        assert bonuses.str_damage == 0
        assert bonuses.str_minor_test == "1-2"
        assert bonuses.str_major_test == "2%"
        assert bonuses.dex_ac_adj == 0
        assert bonuses.con_hp_mod == 0

    def test_high_str_fighter(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=18,
            dexterity=10,
            constitution=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            exceptional_strength=75,
        )
        bonuses = calc.calculate_ability_bonuses(scores, ClassName.FIGHTER)
        assert bonuses.str_to_hit == 2
        assert bonuses.str_damage == 3
        assert bonuses.str_encumbrance == 160
        assert bonuses.str_minor_test == "1-4"
        assert bonuses.str_major_test == "25%"

    def test_exceptional_str_100(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=18,
            dexterity=10,
            constitution=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            exceptional_strength=100,
        )
        bonuses = calc.calculate_ability_bonuses(scores, ClassName.FIGHTER)
        assert bonuses.str_to_hit == 3
        assert bonuses.str_damage == 6
        assert bonuses.str_minor_test == "1-5**"
        assert bonuses.str_major_test == "40%"

    def test_fighter_con_17_gets_plus3(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=17,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        bonuses = calc.calculate_ability_bonuses(scores, ClassName.FIGHTER)
        assert bonuses.con_hp_mod == 3

    def test_nonfighter_con_17_gets_plus2(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=17,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        bonuses = calc.calculate_ability_bonuses(scores, ClassName.CLERIC)
        assert bonuses.con_hp_mod == 2

    def test_high_dex_ac(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=18,
            constitution=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        bonuses = calc.calculate_ability_bonuses(scores, ClassName.THIEF)
        assert bonuses.dex_ac_adj == -4  # descending (better)

    def test_wisdom_bonus_spells(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=10,
            dexterity=10,
            constitution=10,
            intelligence=10,
            wisdom=16,
            charisma=10,
        )
        bonuses = calc.calculate_ability_bonuses(scores, ClassName.CLERIC)
        assert bonuses.wis_mental_save == 2
        assert len(bonuses.wis_bonus_spells) == 4  # +1 lvl1, +1 lvl1, +1 lvl2, +1 lvl2


class TestArmorClass:
    def test_no_armor(self, calc: DerivedStatsCalculator) -> None:
        desc, asc = calc.calculate_armor_class(None, None, 0)
        assert desc == 10
        assert asc == 10

    def test_chain_mail(self, calc: DerivedStatsCalculator) -> None:
        armor = ArmorItem(
            name="Chain Mail",
            ac_desc=5,
            ac_asc=15,
            weight=30.0,
            cost_gp=75.0,
            movement_cap=90,
        )
        desc, asc = calc.calculate_armor_class(armor, None, 0)
        assert desc == 5
        assert asc == 15

    def test_chain_mail_with_shield_and_dex(
        self,
        calc: DerivedStatsCalculator,
    ) -> None:
        armor = ArmorItem(
            name="Chain Mail",
            ac_desc=5,
            ac_asc=15,
            weight=30.0,
            cost_gp=75.0,
            movement_cap=90,
        )
        shield = EquipmentItem(name="Small Shield", weight=5.0, cost_gp=10.0)
        desc, asc = calc.calculate_armor_class(armor, shield, -2)
        assert desc == 2  # 5 - 1 (shield) - 2 (DEX)
        assert asc == 18


class TestSavingThrows:
    def test_fighter_level_1(self, calc: DerivedStatsCalculator) -> None:
        saves = calc.calculate_saving_throws(ClassName.FIGHTER, 1, 0)
        assert saves.aimed_magic_items == 16
        assert saves.breath_weapons == 17
        assert saves.death_paralysis_poison == 14
        assert saves.petrifaction_polymorph == 15
        assert saves.spells == 17

    def test_fighter_level_5(self, calc: DerivedStatsCalculator) -> None:
        saves = calc.calculate_saving_throws(ClassName.FIGHTER, 5, 0)
        assert saves.aimed_magic_items == 13
        assert saves.breath_weapons == 13
        assert saves.death_paralysis_poison == 11
        assert saves.petrifaction_polymorph == 12
        assert saves.spells == 14

    def test_paladin_level_10(self, calc: DerivedStatsCalculator) -> None:
        saves = calc.calculate_saving_throws(ClassName.PALADIN, 10, 0)
        assert saves.aimed_magic_items == 8
        assert saves.breath_weapons == 7

    def test_thief_level_9(self, calc: DerivedStatsCalculator) -> None:
        saves = calc.calculate_saving_throws(ClassName.THIEF, 9, 0)
        assert saves.aimed_magic_items == 10
        assert saves.death_paralysis_poison == 11

    def test_wis_modifier_applies_to_spells(
        self,
        calc: DerivedStatsCalculator,
    ) -> None:
        saves = calc.calculate_saving_throws(ClassName.CLERIC, 1, 3)
        assert saves.spells == 12  # 15 - 3

    def test_stalwart_bonus_for_dwarf(self, calc: DerivedStatsCalculator) -> None:
        saves = calc.calculate_saving_throws(
            ClassName.FIGHTER,
            1,
            0,
            ancestry=AncestryName.DWARF,
            constitution=14,
        )
        # CON 14 → stalwart +4
        assert saves.aimed_magic_items == 12  # 16 - 4
        assert saves.death_paralysis_poison == 10  # 14 - 4
        assert saves.spells == 13  # 17 - 4
        # Breath and petri unaffected
        assert saves.breath_weapons == 17
        assert saves.petrifaction_polymorph == 15


class TestThac0:
    def test_fighter_thac0(self, calc: DerivedStatsCalculator) -> None:
        thac0, bthb = calc.calculate_thac0(ClassName.FIGHTER, 1)
        assert thac0 == 20
        assert bthb == 0

    def test_thief_thac0(self, calc: DerivedStatsCalculator) -> None:
        thac0, bthb = calc.calculate_thac0(ClassName.THIEF, 1)
        assert thac0 == 21
        assert bthb == -1

    def test_fighter_level_5(self, calc: DerivedStatsCalculator) -> None:
        thac0, bthb = calc.calculate_thac0(ClassName.FIGHTER, 5)
        assert thac0 == 16
        assert bthb == 4

    def test_thief_level_9(self, calc: DerivedStatsCalculator) -> None:
        thac0, bthb = calc.calculate_thac0(ClassName.THIEF, 9)
        assert thac0 == 16
        assert bthb == 4

    def test_magic_user_level_16(self, calc: DerivedStatsCalculator) -> None:
        thac0, bthb = calc.calculate_thac0(ClassName.MAGIC_USER, 16)
        assert thac0 == 11
        assert bthb == 9


class TestEncumbrance:
    def test_unencumbered(self, calc: DerivedStatsCalculator) -> None:
        status, move = calc.calculate_encumbrance(30.0, 35, 120, 120)
        assert status == "Unencumbered"
        assert move == 120

    def test_light_encumbrance(self, calc: DerivedStatsCalculator) -> None:
        status, move = calc.calculate_encumbrance(60.0, 35, 120, 120)
        assert status == "Light"
        assert move == 90

    def test_moderate_with_armor_cap(self, calc: DerivedStatsCalculator) -> None:
        status, move = calc.calculate_encumbrance(100.0, 35, 120, 90)
        assert status == "Moderate"
        assert move == 60

    def test_immobile(self, calc: DerivedStatsCalculator) -> None:
        status, move = calc.calculate_encumbrance(200.0, 35, 120, 90)
        assert status == "Immobile"
        assert move == 0


class TestThiefSkills:
    def test_base_human_thief(self, calc: DerivedStatsCalculator) -> None:
        skills = calc.calculate_thief_skills(ClassName.THIEF, AncestryName.HUMAN, 14, 1)
        # Human: +5 climb, +5 pick_locks
        assert skills.climb == 90
        assert skills.pick_locks == 30
        assert skills.hide == 10

    def test_halfling_thief_high_dex(self, calc: DerivedStatsCalculator) -> None:
        skills = calc.calculate_thief_skills(ClassName.THIEF, AncestryName.HALFLING, 18, 1)
        # Base hide=10to +15 ancestry +10 dex = 35
        assert skills.hide == 35
        # Base move_quietly=15 +15 ancestry +10 dex = 40
        assert skills.move_quietly == 40

    def test_monk_no_pick_pockets(self, calc: DerivedStatsCalculator) -> None:
        skills = calc.calculate_thief_skills(ClassName.MONK, AncestryName.HUMAN, 15, 1)
        assert skills.pick_pockets == 1
        assert skills.read_languages == 1

    def test_minimum_one_pct(self, calc: DerivedStatsCalculator) -> None:
        # Low DEX + bad ancestry should never go below 1
        skills = calc.calculate_thief_skills(ClassName.THIEF, AncestryName.DWARF, 9, 1)
        for field in ThiefSkills.model_fields:
            assert getattr(skills, field) >= 1

    def test_thief_level_5(self, calc: DerivedStatsCalculator) -> None:
        skills = calc.calculate_thief_skills(ClassName.THIEF, AncestryName.HUMAN, 14, 5)
        # Level 5 base: climb=89, hide=31, pick_locks=42
        # Human: +5 climb, +5 pick_locks
        assert skills.climb == 94
        assert skills.hide == 31
        assert skills.pick_locks == 47

    def test_thief_level_10(self, calc: DerivedStatsCalculator) -> None:
        skills = calc.calculate_thief_skills(ClassName.THIEF, AncestryName.HUMAN, 14, 10)
        # Level 10 base: pick_pockets=80
        assert skills.pick_pockets == 80


class TestTurnUndead:
    def test_cleric_level_1(self, calc: DerivedStatsCalculator) -> None:
        table = calc.calculate_turn_undead(1)
        assert len(table) >= 5
        assert table[0].roll_needed == 10
        # Type 6 (Ghast) cannot be turned at level 1
        types = [e.undead_type for e in table]
        assert "Type 6" not in types

    def test_cleric_level_4_has_auto_turn(self, calc: DerivedStatsCalculator) -> None:
        table = calc.calculate_turn_undead(4)
        rolls = [e.roll_needed for e in table]
        assert "T" in rolls

    def test_cleric_level_9_has_destroy(self, calc: DerivedStatsCalculator) -> None:
        table = calc.calculate_turn_undead(9)
        rolls = [e.roll_needed for e in table]
        assert "D" in rolls

    def test_cleric_level_9_more_entries_than_1(self, calc: DerivedStatsCalculator) -> None:
        t1 = calc.calculate_turn_undead(1)
        t9 = calc.calculate_turn_undead(9)
        assert len(t9) > len(t1)


class TestSpellSlots:
    def test_cleric_with_wis_16(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.CLERIC, 1, 16)
        assert slots is not None
        # WIS 16: +1(wis13) + 1(wis14) level-1 bonus
        # Level-2 bonus not applicable at level 1 (no base level-2 slots)
        assert slots.level_1 == 3  # 1 base + 2 bonus
        assert slots.level_2 == 0  # no base slots = no bonus

    def test_fighter_no_spells(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.FIGHTER, 1, 10)
        assert slots is None

    def test_magic_user_no_wis_bonus(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.MAGIC_USER, 1, 18)
        assert slots is not None
        assert slots.level_1 == 1  # No WIS bonus

    def test_druid_base_two_slots(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.DRUID, 1, 12)
        assert slots is not None
        assert slots.level_1 == 2

    def test_cleric_level_9(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.CLERIC, 9, 10)
        assert slots is not None
        assert slots.level_1 == 4
        assert slots.level_2 == 4
        assert slots.level_3 == 3
        assert slots.level_4 == 2
        assert slots.level_5 == 1

    def test_magic_user_level_14(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.MAGIC_USER, 14, 10)
        assert slots is not None
        assert slots.level_1 == 5
        assert slots.level_7 == 1

    def test_paladin_no_spells_at_8(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.PALADIN, 8, 10)
        assert slots is None

    def test_paladin_gets_spells_at_9(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.PALADIN, 9, 10)
        assert slots is not None
        assert slots.level_1 == 1

    def test_ranger_no_spells_at_7(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.RANGER, 7, 10)
        assert slots is None

    def test_ranger_druid_spells_at_8(self, calc: DerivedStatsCalculator) -> None:
        slots = calc.calculate_spell_slots(ClassName.RANGER, 8, 10)
        assert slots is not None
        assert slots.level_1 == 1  # 1 druid spell


class TestProficiencySlots:
    def test_fighter_level_1(self, calc: DerivedStatsCalculator) -> None:
        assert calc.calculate_proficiency_slots(ClassName.FIGHTER, 1) == 4

    def test_fighter_level_3(self, calc: DerivedStatsCalculator) -> None:
        assert calc.calculate_proficiency_slots(ClassName.FIGHTER, 3) == 5

    def test_thief_level_6(self, calc: DerivedStatsCalculator) -> None:
        assert calc.calculate_proficiency_slots(ClassName.THIEF, 6) == 3

    def test_magic_user_level_1(self, calc: DerivedStatsCalculator) -> None:
        assert calc.calculate_proficiency_slots(ClassName.MAGIC_USER, 1) == 1


class TestBackstabMultiplier:
    def test_level_1(self, calc: DerivedStatsCalculator) -> None:
        assert calc.calculate_backstab_multiplier(1) == 2

    def test_level_5(self, calc: DerivedStatsCalculator) -> None:
        assert calc.calculate_backstab_multiplier(5) == 3

    def test_level_13(self, calc: DerivedStatsCalculator) -> None:
        assert calc.calculate_backstab_multiplier(13) == 5


class TestXPBonus:
    def test_fighter_str_16_gets_bonus(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=16,
            dexterity=10,
            constitution=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        assert calc.calculate_xp_bonus(ClassName.FIGHTER, scores) == 10

    def test_fighter_str_15_no_bonus(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=15,
            dexterity=10,
            constitution=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
        )
        assert calc.calculate_xp_bonus(ClassName.FIGHTER, scores) == 0

    def test_ranger_all_high(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=16,
            dexterity=10,
            constitution=14,
            intelligence=16,
            wisdom=16,
            charisma=10,
        )
        assert calc.calculate_xp_bonus(ClassName.RANGER, scores) == 10

    def test_ranger_one_low(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=16,
            dexterity=10,
            constitution=14,
            intelligence=15,
            wisdom=16,
            charisma=10,
        )
        assert calc.calculate_xp_bonus(ClassName.RANGER, scores) == 0

    def test_assassin_no_prime(self, calc: DerivedStatsCalculator) -> None:
        scores = AbilityScores(
            strength=18,
            dexterity=18,
            constitution=18,
            intelligence=18,
            wisdom=18,
            charisma=18,
        )
        assert calc.calculate_xp_bonus(ClassName.ASSASSIN, scores) == 0
