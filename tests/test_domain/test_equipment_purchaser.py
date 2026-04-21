"""Tests for EquipmentPurchaser."""

import pytest

from osric_character_gen.domain.equipment_purchaser import EquipmentPurchaser
from osric_character_gen.models.character import ClassName


@pytest.fixture
def purchaser() -> EquipmentPurchaser:
    return EquipmentPurchaser()


class TestEquipmentPurchaser:
    def test_fighter_with_good_budget(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.FIGHTER, 120.0, 14)
        assert loadout.armor is not None
        assert loadout.shield is not None
        assert len(loadout.weapons) >= 1
        assert loadout.gold_remaining >= 0

    def test_fighter_buys_best_armor_affordable(
        self,
        purchaser: EquipmentPurchaser,
    ) -> None:
        loadout = purchaser.purchase_equipment(ClassName.FIGHTER, 150.0, 14)
        assert loadout.armor is not None
        # With 150gp, can afford Banded (AC 4, 90gp) or Splint (AC 4, 80gp)
        # Both are AC 4; lighter one preferred
        assert loadout.armor.ac_desc <= 5

    def test_magic_user_no_armor(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.MAGIC_USER, 40.0, 8)
        assert loadout.armor is None
        assert loadout.shield is None

    def test_magic_user_gets_dagger(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.MAGIC_USER, 40.0, 8)
        weapon_names = [w.name for w in loadout.weapons]
        assert "Dagger" in weapon_names or "Staff" in weapon_names

    def test_cleric_gets_holy_symbol(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.CLERIC, 120.0, 10)
        eq_names = [e.name for e in loadout.equipment]
        assert "Holy symbol, pewter" in eq_names

    def test_thief_gets_thieves_tools(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.THIEF, 100.0, 10)
        eq_names = [e.name for e in loadout.equipment]
        assert "Thieves' tools" in eq_names

    def test_monk_very_low_budget(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.MONK, 8.0, 12)
        assert loadout.armor is None
        assert loadout.gold_remaining >= 0

    def test_budget_not_exceeded(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.FIGHTER, 50.0, 10)
        assert loadout.gold_remaining >= 0

    def test_weight_tracked(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.FIGHTER, 120.0, 14)
        assert loadout.total_weight > 0

    def test_thief_restricted_armor(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.THIEF, 100.0, 10)
        if loadout.armor:
            assert loadout.armor.name in ["Leather", "Padded", "Studded Leather"]

    def test_druid_leather_only(self, purchaser: EquipmentPurchaser) -> None:
        loadout = purchaser.purchase_equipment(ClassName.DRUID, 100.0, 10)
        if loadout.armor:
            assert loadout.armor.name == "Leather"

    def test_remaining_gold_not_in_weight(self, purchaser: EquipmentPurchaser) -> None:
        """Remaining gold should NOT be counted in carried weight."""
        loadout_rich = purchaser.purchase_equipment(ClassName.MAGIC_USER, 500.0, 8)
        loadout_poor = purchaser.purchase_equipment(ClassName.MAGIC_USER, 40.0, 8)
        # Rich loadout has much more gold remaining but equipment weight
        # should be similar since they buy the same gear
        # The difference in total_weight should NOT include coin weight
        gold_diff = loadout_rich.gold_remaining - loadout_poor.gold_remaining
        weight_diff = loadout_rich.total_weight - loadout_poor.total_weight
        # If gold were counted, weight_diff would be ~gold_diff/10
        # Without gold, weight_diff should be small (just extra gear bought)
        assert weight_diff < gold_diff / 10.0, (
            f"Gold seems to be counted in weight: weight_diff={weight_diff:.1f}, gold_diff={gold_diff:.1f}"
        )
