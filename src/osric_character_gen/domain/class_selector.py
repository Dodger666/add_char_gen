"""Class selection logic for OSRIC 3.0 character generation."""

from osric_character_gen.data.classes import (
    CLASS_MINIMUMS,
    CLASS_PRIME_REQUISITES,
    CLASS_PRIORITY,
)
from osric_character_gen.models.character import AbilityScores, ClassName


class NoEligibleClassError(Exception):
    """Raised when no class qualifies for the given ability scores."""


class ClassSelector:
    def get_eligible_classes(self, scores: AbilityScores) -> list[ClassName]:
        """Return all classes whose minimum requirements are met."""
        eligible = []
        score_dict = {
            "strength": scores.strength,
            "dexterity": scores.dexterity,
            "constitution": scores.constitution,
            "intelligence": scores.intelligence,
            "wisdom": scores.wisdom,
            "charisma": scores.charisma,
        }
        for class_name, minimums in CLASS_MINIMUMS.items():
            qualifies = True
            for ability, minimum in minimums.items():
                if minimum is not None and score_dict[ability] < minimum:
                    qualifies = False
                    break
            if qualifies:
                eligible.append(class_name)
        return eligible

    def score_class(self, class_name: ClassName, scores: AbilityScores) -> int:
        """Calculate prime requisite score for a class."""
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
        return min(score_dict[attr] for attr in prime_reqs)

    def select_best_class(self, scores: AbilityScores) -> ClassName:
        """Select the class with the highest prime requisite score."""
        eligible = self.get_eligible_classes(scores)
        if not eligible:
            raise NoEligibleClassError("No class qualifies for these scores")

        # Separate classes with and without prime requisites
        with_prime = [c for c in eligible if CLASS_PRIME_REQUISITES[c]]
        without_prime = [c for c in eligible if not CLASS_PRIME_REQUISITES[c]]

        if with_prime:
            # Score and sort by prime requisite, then by priority
            best_score = -1
            best_class = with_prime[0]
            for cls in CLASS_PRIORITY:
                if cls in with_prime:
                    score = self.score_class(cls, scores)
                    if score > best_score:
                        best_score = score
                        best_class = cls
            return best_class

        # No prime requisite classes: Monk > Illusionist > Assassin
        no_prime_priority = [ClassName.MONK, ClassName.ILLUSIONIST, ClassName.ASSASSIN]
        for cls in no_prime_priority:
            if cls in without_prime:
                return cls

        return without_prime[0]
