"""Ancestry selection logic for OSRIC 3.0 character generation."""

from osric_character_gen.data.ancestries import (
    ANCESTRY_ADJUSTMENTS,
    ANCESTRY_CLASSES,
    ANCESTRY_PREFERENCE,
    ANCESTRY_SCORE_RANGES,
)
from osric_character_gen.data.classes import CLASS_MINIMUMS
from osric_character_gen.models.character import AbilityScores, AncestryName, ClassName


class AncestrySelector:
    def get_eligible_ancestries(self, class_name: ClassName, scores: AbilityScores) -> list[AncestryName]:
        """Return ancestries that can play the given class
        AND whose score ranges are satisfied after adjustments."""
        eligible = []
        for ancestry in AncestryName:
            if class_name not in ANCESTRY_CLASSES[ancestry]:
                continue
            adjusted = self.apply_adjustments(scores, ancestry)
            if self.validate_scores(adjusted, ancestry, class_name):
                eligible.append(ancestry)
        return eligible

    def select_best_ancestry(self, class_name: ClassName, scores: AbilityScores) -> AncestryName:
        """Select optimal ancestry for the class/score combination."""
        eligible = self.get_eligible_ancestries(class_name, scores)
        if not eligible:
            return AncestryName.HUMAN

        preference = ANCESTRY_PREFERENCE.get(class_name, [AncestryName.HUMAN])
        for preferred in preference:
            if preferred in eligible:
                return preferred

        # Fallback: Human if eligible, else first eligible
        if AncestryName.HUMAN in eligible:
            return AncestryName.HUMAN
        return eligible[0]

    def apply_adjustments(self, scores: AbilityScores, ancestry: AncestryName) -> AbilityScores:
        """Return new AbilityScores with ancestral adjustments applied."""
        adjustments = ANCESTRY_ADJUSTMENTS[ancestry]
        if not adjustments:
            return scores

        return AbilityScores(
            strength=scores.strength + adjustments.get("strength", 0),
            dexterity=scores.dexterity + adjustments.get("dexterity", 0),
            constitution=scores.constitution + adjustments.get("constitution", 0),
            intelligence=scores.intelligence + adjustments.get("intelligence", 0),
            wisdom=scores.wisdom + adjustments.get("wisdom", 0),
            charisma=scores.charisma + adjustments.get("charisma", 0),
            exceptional_strength=scores.exceptional_strength,
        )

    def validate_scores(self, scores: AbilityScores, ancestry: AncestryName, class_name: ClassName) -> bool:
        """Verify adjusted scores meet both ancestry ranges and class minimums."""
        ranges = ANCESTRY_SCORE_RANGES[ancestry]
        minimums = CLASS_MINIMUMS[class_name]
        score_dict = {
            "strength": scores.strength,
            "dexterity": scores.dexterity,
            "constitution": scores.constitution,
            "intelligence": scores.intelligence,
            "wisdom": scores.wisdom,
            "charisma": scores.charisma,
        }

        for ability, (low, high) in ranges.items():
            val = score_dict[ability]
            if val < low or val > high:
                return False

        return all(not (minimum is not None and score_dict[ability] < minimum) for ability, minimum in minimums.items())
