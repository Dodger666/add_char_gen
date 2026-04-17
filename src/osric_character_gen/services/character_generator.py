"""Character generation service — main orchestrator."""

import random

from osric_character_gen.data.ancestries import (
    ANCESTRY_FEATURES,
    ANCESTRY_LANGUAGES,
    ANCESTRY_MOVEMENT,
)
from osric_character_gen.data.classes import (
    CLASS_HIT_DICE_COUNT,
    CLASS_HIT_DIE,
    CLASS_PROFICIENCY_SLOTS,
    CLASS_STARTING_GOLD,
)
from osric_character_gen.domain.ancestry_selector import AncestrySelector
from osric_character_gen.domain.class_selector import (
    ClassSelector,
    NoEligibleClassError,
)
from osric_character_gen.domain.dice import DiceRoller
from osric_character_gen.domain.equipment_purchaser import EquipmentPurchaser
from osric_character_gen.domain.name_generator import HolmesianNameGenerator
from osric_character_gen.domain.physical_generator import (
    PhysicalCharacteristicsGenerator,
)
from osric_character_gen.domain.spell_selector import SpellSelector
from osric_character_gen.domain.stats_calculator import DerivedStatsCalculator
from osric_character_gen.models.character import (
    AbilityScores,
    CharacterSheet,
    ClassName,
)


class MaxRetriesExceededError(Exception):
    """Raised when character generation fails after maximum retries."""


class CharacterGeneratorService:
    MAX_RETRIES = 100

    def __init__(self) -> None:
        self._class_selector = ClassSelector()
        self._ancestry_selector = AncestrySelector()
        self._equipment_purchaser = EquipmentPurchaser()
        self._stats_calculator = DerivedStatsCalculator()

    def generate(self, seed: int | None = None) -> tuple[CharacterSheet, dict]:
        """Main generation entry point."""
        if seed is None:
            seed = random.randint(0, 2**31 - 1)

        roller = DiceRoller(seed=seed)
        spell_selector = SpellSelector(roller)
        physical_gen = PhysicalCharacteristicsGenerator(roller)

        metadata: dict = {"retries": 0, "seed": seed}

        # Retry loop
        scores = None
        class_name = None
        ancestry = None
        adjusted_scores = None

        for attempt in range(self.MAX_RETRIES):
            # Step 1: Roll ability scores
            raw = roller.roll_ability_scores()
            scores = AbilityScores(
                strength=raw[0],
                dexterity=raw[1],
                constitution=raw[2],
                intelligence=raw[3],
                wisdom=raw[4],
                charisma=raw[5],
            )

            # Step 2-3: Select class
            try:
                class_name = self._class_selector.select_best_class(scores)
            except NoEligibleClassError:
                metadata["retries"] = attempt + 1
                continue

            # Step 4-5: Select ancestry
            ancestry = self._ancestry_selector.select_best_ancestry(class_name, scores)

            # Step 6: Apply ancestral adjustments
            adjusted_scores = self._ancestry_selector.apply_adjustments(scores, ancestry)

            # Step 7: Validate
            if self._ancestry_selector.validate_scores(adjusted_scores, ancestry, class_name):
                metadata["retries"] = attempt
                break
        else:
            raise MaxRetriesExceededError(f"Failed to generate valid character after {self.MAX_RETRIES} attempts")

        assert class_name is not None
        assert ancestry is not None
        assert adjusted_scores is not None

        # Step 8: Exceptional strength
        fighter_types = {ClassName.FIGHTER, ClassName.PALADIN, ClassName.RANGER}
        if class_name in fighter_types and adjusted_scores.strength == 18:
            exceptional = roller.roll_percentile()
            adjusted_scores = AbilityScores(
                strength=adjusted_scores.strength,
                dexterity=adjusted_scores.dexterity,
                constitution=adjusted_scores.constitution,
                intelligence=adjusted_scores.intelligence,
                wisdom=adjusted_scores.wisdom,
                charisma=adjusted_scores.charisma,
                exceptional_strength=exceptional,
            )

        # Step 9: Calculate ability bonuses (needed for HP)
        bonuses = self._stats_calculator.calculate_ability_bonuses(adjusted_scores, class_name)

        # Step 10: Roll hit points
        hit_die = CLASS_HIT_DIE[class_name]
        dice_count = CLASS_HIT_DICE_COUNT[class_name]
        min_die_val = 2 if adjusted_scores.constitution >= 19 else 1
        hit_points = roller.roll_hit_points(hit_die, bonuses.con_hp_mod, dice_count, min_die_val)

        # Step 11: Select alignment
        from osric_character_gen.data.classes import CLASS_ALIGNMENTS

        alignment = roller.choice(CLASS_ALIGNMENTS[class_name])

        # Step 12: Roll starting gold
        gold_dice, gold_sides, gold_mult = CLASS_STARTING_GOLD[class_name]
        starting_gold = roller.roll_gold(gold_dice, gold_sides, gold_mult)

        # Step 13: Purchase equipment
        loadout = self._equipment_purchaser.purchase_equipment(class_name, starting_gold, adjusted_scores.strength)

        # Step 14: Calculate derived stats
        ac_desc, ac_asc = self._stats_calculator.calculate_armor_class(
            loadout.armor, loadout.shield, bonuses.dex_ac_adj
        )

        saving_throws = self._stats_calculator.calculate_saving_throws(
            class_name,
            1,
            bonuses.wis_mental_save,
            ancestry=ancestry,
            constitution=adjusted_scores.constitution,
        )

        thac0, bthb = self._stats_calculator.calculate_thac0(class_name, 1)

        base_movement = ANCESTRY_MOVEMENT[ancestry]
        armor_cap = loadout.armor.movement_cap if loadout.armor else 999
        encumbrance_status, effective_movement = self._stats_calculator.calculate_encumbrance(
            loadout.total_weight,
            bonuses.str_encumbrance,
            base_movement,
            armor_cap,
        )

        # Thief/Assassin/Monk skills
        thief_skill_classes = {ClassName.THIEF, ClassName.ASSASSIN, ClassName.MONK}
        thief_skills = None
        if class_name in thief_skill_classes:
            thief_skills = self._stats_calculator.calculate_thief_skills(
                class_name, ancestry, adjusted_scores.dexterity
            )

        # Turn undead
        turn_undead = None
        if class_name == ClassName.CLERIC:
            turn_undead = self._stats_calculator.calculate_turn_undead(1)

        # Spell slots and spells
        spell_slots = self._stats_calculator.calculate_spell_slots(class_name, 1, adjusted_scores.wisdom)
        spells_memorized, spellbook = spell_selector.select_starting_spells(class_name, spell_slots)

        # XP bonus
        xp_bonus = self._stats_calculator.calculate_xp_bonus(class_name, adjusted_scores)

        # Step 15: Physical characteristics
        physical = physical_gen.generate(ancestry, class_name)

        # Step 16: Age category adjustments
        age_adj = physical_gen.get_age_adjustments(physical.age_category)
        if age_adj:
            from osric_character_gen.data.ancestries import ANCESTRY_SCORE_RANGES

            ranges = ANCESTRY_SCORE_RANGES[ancestry]
            final_str = max(
                ranges["strength"][0],
                min(ranges["strength"][1], adjusted_scores.strength + age_adj.get("strength", 0)),
            )
            final_dex = max(
                ranges["dexterity"][0],
                min(ranges["dexterity"][1], adjusted_scores.dexterity + age_adj.get("dexterity", 0)),
            )
            final_con = max(
                ranges["constitution"][0],
                min(ranges["constitution"][1], adjusted_scores.constitution + age_adj.get("constitution", 0)),
            )
            final_int = max(
                ranges["intelligence"][0],
                min(ranges["intelligence"][1], adjusted_scores.intelligence + age_adj.get("intelligence", 0)),
            )
            final_wis = max(
                ranges["wisdom"][0],
                min(ranges["wisdom"][1], adjusted_scores.wisdom + age_adj.get("wisdom", 0)),
            )
            exc_str = adjusted_scores.exceptional_strength
            if exc_str is not None and age_adj.get("strength", 0) < 0:
                exc_str = None  # Lose exceptional on strength decrease

            adjusted_scores = AbilityScores(
                strength=final_str,
                dexterity=final_dex,
                constitution=final_con,
                intelligence=final_int,
                wisdom=final_wis,
                charisma=adjusted_scores.charisma,
                exceptional_strength=exc_str,
            )
            # Recalculate bonuses after age adjustments
            bonuses = self._stats_calculator.calculate_ability_bonuses(adjusted_scores, class_name)

        # Weapon proficiencies
        prof_slots = CLASS_PROFICIENCY_SLOTS[class_name]
        weapon_profs = [w.name for w in loadout.weapons[:prof_slots]]

        # Class features
        class_features = self._build_class_features(class_name, spell_slots, bonuses, adjusted_scores)

        # Languages
        languages = list(ANCESTRY_LANGUAGES[ancestry])

        # Character name (Holmesian Random Names)
        name_gen = HolmesianNameGenerator(roller)
        character_name = name_gen.generate(include_title=True)

        # Build the character sheet
        sheet = CharacterSheet(
            name=character_name,
            character_class=class_name,
            level=1,
            alignment=alignment,
            ancestry=ancestry,
            xp=0,
            xp_bonus_pct=xp_bonus,
            hit_points=hit_points,
            armor_class_desc=ac_desc,
            armor_class_asc=ac_asc,
            physical=physical,
            ability_scores=adjusted_scores,
            ability_bonuses=bonuses,
            thac0=thac0,
            bthb=bthb,
            saving_throws=saving_throws,
            melee_to_hit_mod=bonuses.str_to_hit,
            missile_to_hit_mod=bonuses.dex_missile_to_hit,
            armor=loadout.armor,
            shield=loadout.shield,
            weapons=loadout.weapons,
            equipment=loadout.equipment,
            gold_remaining=loadout.gold_remaining,
            total_weight_lbs=loadout.total_weight,
            encumbrance_allowance=bonuses.str_encumbrance,
            encumbrance_status=encumbrance_status,
            base_movement=base_movement,
            effective_movement=effective_movement,
            thief_skills=thief_skills,
            turn_undead=turn_undead,
            spell_slots=spell_slots,
            spells_memorized=spells_memorized if spells_memorized else None,
            spellbook=spellbook,
            ancestry_features=ANCESTRY_FEATURES[ancestry],
            class_features=class_features,
            weapon_proficiencies=weapon_profs,
            languages=languages,
            generation_seed=seed,
        )

        # Metadata
        eligible_classes = self._class_selector.get_eligible_classes(adjusted_scores)
        class_scores = {}
        for cls in eligible_classes:
            class_scores[cls.value] = self._class_selector.score_class(cls, adjusted_scores)
        metadata["eligible_classes"] = [c.value for c in eligible_classes]
        metadata["class_scores"] = class_scores
        metadata["selected_class"] = class_name.value
        metadata["selected_ancestry"] = ancestry.value

        return sheet, metadata

    def _build_class_features(
        self,
        class_name: ClassName,
        spell_slots,
        bonuses,
        scores: AbilityScores,
    ) -> list[str]:
        """Build list of class features for display."""
        features = []

        if class_name == ClassName.CLERIC:
            features.append("Turn Undead")
            if spell_slots:
                features.append(f"Divine Spellcasting ({spell_slots.level_1} first-level slots)")

        elif class_name == ClassName.DRUID:
            if spell_slots:
                features.append(f"Druidic Spellcasting ({spell_slots.level_1} first-level slots)")

        elif class_name == ClassName.MAGIC_USER:
            if spell_slots:
                features.append(f"Arcane Spellcasting ({spell_slots.level_1} first-level slots)")
            features.append("Spellbook (4 starting spells)")

        elif class_name == ClassName.ILLUSIONIST:
            if spell_slots:
                features.append(f"Phantasmal Spellcasting ({spell_slots.level_1} first-level slots)")
            features.append("Spellbook (3 starting spells)")

        elif class_name == ClassName.THIEF:
            features.append("Backstab (×2 damage)")
            features.append("Thief Skills")

        elif class_name == ClassName.ASSASSIN:
            features.append("Assassination")
            features.append("Backstab (×2 damage)")
            features.append("Thief Skills")

        elif class_name == ClassName.MONK:
            features.append("Monk AC 10 at level 1")
            features.append("Weaponless combat: 1d3 damage")
            features.append("Thief Skills (limited)")
            features.append("Movement Rate: 150 ft")

        elif class_name == ClassName.PALADIN:
            features.append("+2 to all saving throws (built into table)")
            features.append("Detect Evil (60 ft)")
            features.append("Lay on Hands (2 HP per level per day)")
            features.append("Immune to disease")

        elif class_name == ClassName.RANGER:
            features.append("+1 damage per level vs giant-class creatures")
            features.append("Tracking")
            features.append("Surprise on 1-3 (d6)")

        elif class_name == ClassName.FIGHTER:
            features.append("Weapon specialization available (not implemented)")

        return features
