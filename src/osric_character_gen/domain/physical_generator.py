"""Physical characteristics generator for OSRIC 3.0 character generation."""

from osric_character_gen.data.ancestries import (
    AGE_CATEGORY_ADJUSTMENTS,
    ANCESTRY_AGE_CATEGORIES,
    ANCESTRY_HEIGHT,
    ANCESTRY_STARTING_AGE,
    ANCESTRY_WEIGHT,
)
from osric_character_gen.domain.dice import DiceRoller
from osric_character_gen.models.character import (
    AncestryName,
    ClassName,
    Gender,
    PhysicalCharacteristics,
)


class PhysicalCharacteristicsGenerator:
    def __init__(self, roller: DiceRoller) -> None:
        self._roller = roller

    def generate(self, ancestry: AncestryName, class_name: ClassName) -> PhysicalCharacteristics:
        """Roll height, weight, starting age, determine age category, gender."""
        height_inches = self._roll_height(ancestry)
        weight_lbs = self._roll_weight(ancestry)
        age = self._roll_starting_age(ancestry, class_name)
        age_category = self.get_age_category(ancestry, age)
        gender = self._roller.choice([Gender.MALE, Gender.FEMALE])

        feet = height_inches // 12
        inches = height_inches % 12
        height_display = f"{feet}'{inches}\""

        return PhysicalCharacteristics(
            height_inches=height_inches,
            height_display=height_display,
            weight_lbs=weight_lbs,
            age=age,
            age_category=age_category,
            gender=gender,
        )

    def _roll_height(self, ancestry: AncestryName) -> int:
        base, num_dice, die_sides = ANCESTRY_HEIGHT[ancestry]
        return base + sum(self._roller.roll_multiple(num_dice, die_sides))

    def _roll_weight(self, ancestry: AncestryName) -> int:
        base, num_dice, die_sides = ANCESTRY_WEIGHT[ancestry]
        return base + sum(self._roller.roll_multiple(num_dice, die_sides))

    def _roll_starting_age(self, ancestry: AncestryName, class_name: ClassName) -> int:
        age_data = ANCESTRY_STARTING_AGE.get(ancestry, {})
        if class_name not in age_data:
            # Fallback for missing combos
            return 20
        base, num_dice, die_sides = age_data[class_name]
        return base + sum(self._roller.roll_multiple(num_dice, die_sides))

    def get_age_category(self, ancestry: AncestryName, age: int) -> str:
        """Return age category name."""
        youth_max, adult_min, grizzled_min, elder_min, ancient_min = ANCESTRY_AGE_CATEGORIES[ancestry]
        if age >= ancient_min:
            return "Ancient"
        if age >= elder_min:
            return "Elder"
        if age >= grizzled_min:
            return "Grizzled"
        if age >= adult_min:
            return "Adult"
        return "Youth"

    def get_age_adjustments(self, category: str) -> dict[str, int]:
        """Return ability score adjustments for the age category."""
        return AGE_CATEGORY_ADJUSTMENTS.get(category, {})
