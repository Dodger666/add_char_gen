"""Derived statistics calculator for OSRIC 3.0 character generation."""

from osric_character_gen.data.ability_tables import (
    get_charisma_bonuses,
    get_constitution_bonuses,
    get_dexterity_bonuses,
    get_intelligence_bonuses,
    get_strength_bonuses,
    get_wisdom_bonuses,
)
from osric_character_gen.data.ancestries import STALWART_ANCESTRIES, STALWART_BONUS
from osric_character_gen.data.classes import (
    BACKSTAB_TABLE,
    CLASS_PRIME_REQUISITES,
    CLASS_PROFICIENCY_GAIN_LEVELS,
    CLASS_PROFICIENCY_SLOTS,
    RANGER_DRUID_SLOTS,
    SPELL_SLOT_TABLES,
    XP_BONUS_PERCENT,
    XP_BONUS_THRESHOLD,
    get_thac0,
)
from osric_character_gen.data.saving_throws import get_saving_throws
from osric_character_gen.data.thief_skills import (
    ANCESTRY_THIEF_ADJUSTMENTS,
    DEX_THIEF_ADJUSTMENTS,
    MONK_EXCLUDED_SKILLS,
    THIEF_SKILLS_BY_LEVEL,
)
from osric_character_gen.data.turn_undead import get_turn_undead
from osric_character_gen.models.character import (
    AbilityBonuses,
    AbilityScores,
    AncestryName,
    ArmorItem,
    ClassName,
    EquipmentItem,
    SavingThrows,
    SpellSlots,
    ThiefSkills,
    TurnUndeadEntry,
)


class DerivedStatsCalculator:
    def calculate_ability_bonuses(self, scores: AbilityScores, class_name: ClassName) -> AbilityBonuses:
        """Look up all ability score bonuses from tables."""
        str_hit, str_dmg, str_enc, str_minor, str_major = get_strength_bonuses(
            scores.strength, scores.exceptional_strength
        )
        dex_surprise, dex_missile, dex_init, dex_ac_desc, _dex_ac_asc, _dex_agility = get_dexterity_bonuses(
            scores.dexterity
        )
        con_hp, con_res, con_shock = get_constitution_bonuses(scores.constitution, class_name)
        int_langs = get_intelligence_bonuses(scores.intelligence)
        wis_mental, wis_bonus_spells = get_wisdom_bonuses(scores.wisdom)
        cha_sidekick, cha_loyalty, cha_reaction = get_charisma_bonuses(scores.charisma)

        return AbilityBonuses(
            str_to_hit=str_hit,
            str_damage=str_dmg,
            str_encumbrance=str_enc,
            str_minor_test=str_minor,
            str_major_test=str_major,
            dex_surprise=dex_surprise,
            dex_missile_to_hit=dex_missile,
            dex_ac_adj=dex_ac_desc,
            dex_initiative=dex_init,
            con_hp_mod=con_hp,
            con_resurrection=con_res,
            con_system_shock=con_shock,
            int_max_languages=int_langs,
            wis_mental_save=wis_mental,
            wis_bonus_spells=wis_bonus_spells,
            cha_sidekick_limit=cha_sidekick,
            cha_loyalty_mod=cha_loyalty,
            cha_reaction_mod=cha_reaction,
        )

    def calculate_armor_class(
        self,
        armor: ArmorItem | None,
        shield: EquipmentItem | None,
        dex_ac_adj: int,
    ) -> tuple[int, int]:
        """Return (descending_ac, ascending_ac)."""
        base_desc = 10
        if armor is not None:
            base_desc = armor.ac_desc
        shield_adj = -1 if shield is not None else 0
        final_desc = base_desc + shield_adj + dex_ac_adj
        final_asc = 20 - final_desc
        return final_desc, final_asc

    def calculate_saving_throws(
        self,
        class_name: ClassName,
        level: int,
        wis_mental_save: int,
        ancestry: AncestryName | None = None,
        constitution: int = 10,
    ) -> SavingThrows:
        """Look up base saves and apply modifiers."""
        aimed, breath, death, petri, spells = get_saving_throws(class_name, level)

        # WIS mental save applies to Spells category
        spells_modified = spells - wis_mental_save

        # Stalwart bonus for Dwarf/Gnome/Halfling
        stalwart = 0
        if ancestry in STALWART_ANCESTRIES:
            stalwart = STALWART_BONUS.get(constitution, 0)
            # Applies to aimed magic, death (poison), spells
            aimed -= stalwart
            death -= stalwart
            spells_modified -= stalwart

        return SavingThrows(
            aimed_magic_items=aimed,
            breath_weapons=breath,
            death_paralysis_poison=death,
            petrifaction_polymorph=petri,
            spells=spells_modified,
        )

    def calculate_thac0(self, class_name: ClassName, level: int) -> tuple[int, int]:
        """Return (thac0, bthb)."""
        return get_thac0(class_name, level)

    def calculate_encumbrance(
        self,
        total_weight: float,
        str_encumbrance: int,
        base_movement: int,
        armor_cap: int,
    ) -> tuple[str, int]:
        """Return (encumbrance_status, effective_movement)."""
        overage = total_weight - str_encumbrance
        if overage <= 0:
            status = "Unencumbered"
            move_mult = 1.0
        elif overage <= 40:
            status = "Light"
            move_mult = 0.75
        elif overage <= 80:
            status = "Moderate"
            move_mult = 0.5
        elif overage <= 120:
            status = "Heavy"
            move_mult = 0.25
        else:
            status = "Immobile"
            move_mult = 0.0

        enc_movement = int(base_movement * move_mult)
        effective = min(enc_movement, armor_cap)
        return status, effective

    def calculate_thief_skills(
        self,
        class_name: ClassName,
        ancestry: AncestryName,
        dexterity: int,
        level: int = 1,
    ) -> ThiefSkills:
        """Calculate thief skills with DEX and ancestry adjustments."""
        # Use level-based base values; clamp to max available level (17)
        effective_level = min(level, max(THIEF_SKILLS_BY_LEVEL.keys()))
        skills = dict(THIEF_SKILLS_BY_LEVEL[effective_level])

        # Apply DEX adjustments
        dex_adj = DEX_THIEF_ADJUSTMENTS.get(dexterity, {})
        for skill, adj in dex_adj.items():
            skills[skill] = skills[skill] + adj

        # Apply ancestry adjustments (monks are human-only, no ancestry adj)
        if class_name != ClassName.MONK:
            anc_adj = ANCESTRY_THIEF_ADJUSTMENTS.get(ancestry, {})
            for skill, adj in anc_adj.items():
                skills[skill] = skills[skill] + adj

        # Monks don't get pick_pockets or read_languages
        if class_name == ClassName.MONK:
            for excluded in MONK_EXCLUDED_SKILLS:
                skills[excluded] = 1  # minimum

        # Clamp all to [1, 99]
        for skill in skills:
            skills[skill] = max(1, min(99, skills[skill]))

        return ThiefSkills(**skills)

    def calculate_turn_undead(self, level: int) -> list[TurnUndeadEntry]:
        """Return turn undead table for cleric at given level."""
        entries = get_turn_undead(level)
        return [TurnUndeadEntry(undead_type=t[0], example=t[1], roll_needed=t[2]) for t in entries]

    def calculate_spell_slots(self, class_name: ClassName, level: int, wisdom: int) -> SpellSlots | None:
        """Calculate spell slots including WIS bonus spells."""
        # Ranger has dual spellcasting
        if class_name == ClassName.RANGER:
            return self._calculate_ranger_spell_slots(level)

        # Paladin gets spells at level 9+
        if class_name == ClassName.PALADIN:
            return self._calculate_paladin_spell_slots(level)

        slot_table = SPELL_SLOT_TABLES.get(class_name)
        if slot_table is None:
            return None

        # Find the effective level (clamp to max in table)
        max_table_level = max(slot_table.keys())
        effective_level = min(level, max_table_level)
        base = slot_table[effective_level]

        slots = {f"level_{i + 1}": base[i] for i in range(7)}

        # WIS bonus spells (cleric/druid only)
        if class_name in (ClassName.CLERIC, ClassName.DRUID):
            _, bonus_list = get_wisdom_bonuses(wisdom)
            for bonus in bonus_list:
                level_key = f"level_{bonus['level']}"
                if level_key in slots and slots[level_key] > 0:
                    slots[level_key] += bonus["slots"]

        return SpellSlots(**slots)

    def _calculate_paladin_spell_slots(self, level: int) -> SpellSlots | None:
        """Paladin gets cleric spells at level 9+."""
        slot_table = SPELL_SLOT_TABLES.get(ClassName.PALADIN)
        if slot_table is None or level < 9:
            return None
        max_table_level = max(slot_table.keys())
        effective_level = min(level, max_table_level)
        base = slot_table[effective_level]
        if all(s == 0 for s in base):
            return None
        slots = {f"level_{i + 1}": base[i] for i in range(7)}
        return SpellSlots(**slots)

    def _calculate_ranger_spell_slots(self, level: int) -> SpellSlots | None:
        """Ranger gets druid spells at 8+, magic-user spells at 9+."""
        if level < 8:
            return None
        slots = {f"level_{i}": 0 for i in range(1, 8)}
        # Druid spells (level 8+)
        druid = RANGER_DRUID_SLOTS.get(level)
        if druid is None and level > max(RANGER_DRUID_SLOTS.keys()):
            druid = RANGER_DRUID_SLOTS[max(RANGER_DRUID_SLOTS.keys())]
        if druid:
            for i, val in enumerate(druid):
                slots[f"level_{i + 1}"] += val
        return SpellSlots(**slots)

    def calculate_xp_bonus(self, class_name: ClassName, scores: AbilityScores) -> int:
        """Return 0 or 10 (percent) based on prime requisite values."""
        prime_reqs = CLASS_PRIME_REQUISITES[class_name]
        if not prime_reqs:
            return 0

        score_dict = {
            "strength": scores.strength,
            "dexterity": scores.dexterity,
            "constitution": scores.constitution,
            "intelligence": scores.intelligence,
            "wisdom": scores.wisdom,
            "charisma": scores.charisma,
        }

        for attr in prime_reqs:
            if score_dict[attr] < XP_BONUS_THRESHOLD:
                return 0
        return XP_BONUS_PERCENT

    def calculate_proficiency_slots(self, class_name: ClassName, level: int) -> int:
        """Calculate total weapon proficiency slots at a given level."""
        base = CLASS_PROFICIENCY_SLOTS[class_name]
        gain_levels = CLASS_PROFICIENCY_GAIN_LEVELS[class_name]
        extra = sum(1 for lvl in gain_levels if lvl <= level)
        return base + extra

    def calculate_backstab_multiplier(self, level: int) -> int:
        """Return backstab damage multiplier for thief/assassin level."""
        for max_lvl, mult in BACKSTAB_TABLE:
            if level <= max_lvl:
                return mult
        return BACKSTAB_TABLE[-1][1]
